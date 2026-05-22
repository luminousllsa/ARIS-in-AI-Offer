#!/usr/bin/env python3
"""aris_homepage.py — generate fact-checked academic homepages from a CV.

See skills/homepage-generator/SKILL.md for the full contract.

Pipeline:
    init --from-cv  →  textutil → LLM extract → profile.yml + bib + bio.md + news.md
    render          →  load → fact-check (DBLP/arXiv) → Python build HTML chunks → template render
    check           →  fact-check only, update audit-report.md
    doctor          →  environment + dependency diagnostic

This is a SKELETON (v0). Function bodies are stubbed with TODO markers.
Round-2 cross-model design (Codex GPT-5.5 xhigh + Gemini auto-gemini-3) converged on:
  - macOS textutil for .docx; python-docx as optional fallback
  - LLM extraction via the calling Claude agent (NOT here in Python); persisted via this script
  - JSON-schema-constrained extraction output
  - Idempotency: bail by default if profile.yml exists
  - DBLP direct API call (no third-party lib)
  - Two-layer override: per-paper YAML + --override-all CLI
  - Template approach: Python builds per-section HTML chunks, template only shell

External deps (Python): pyyaml, bibtexparser. Checked by `doctor`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Optional imports — handled gracefully by doctor()
try:
    import yaml  # type: ignore
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

try:
    import bibtexparser  # type: ignore
    HAS_BIBTEXPARSER = True
except ImportError:
    HAS_BIBTEXPARSER = False


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCHEMA_VERSION = 1
DBLP_API = "https://dblp.org/search/publ/api"
ARXIV_API = "http://export.arxiv.org/api/query"

DEFAULT_FILES = {
    "profile": "profile.yml",
    "bib": "publications.bib",
    "bio": "bio.md",
    "news": "news.md",
    "extraction_review": "EXTRACTION_REVIEW.md",
    "audit_report": "audit-report.md",
    "output_html": "index.html",
}

PERSONAS = ("theory-minimal", "active-researcher")
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


# ---------------------------------------------------------------------------
# Command: init --from-cv
# ---------------------------------------------------------------------------

def cmd_init(args: argparse.Namespace) -> int:
    """Bootstrap workspace by extracting a CV into structured editable files.

    Steps:
      1. Convert CV to plain text (textutil for .docx; cat for .txt; PDF via pdftotext).
      2. Hand off to calling LLM agent to extract into JSON (this script only persists).
         The agent reads cv.txt, fills the JSON-schema constrained output, writes back.
      3. This script converts JSON → profile.yml + publications.bib + bio.md + news.md.
      4. Write EXTRACTION_REVIEW.md with confidence flags.

    Idempotency:
      - default: bail if profile.yml exists
      - --force: backup *.bak-TIMESTAMP and overwrite
      - --merge: fill only missing fields; conflicts logged in EXTRACTION_REVIEW.md
    """
    out_dir = Path(args.out).resolve()
    cv_path = Path(args.from_cv).resolve()
    if not cv_path.exists():
        die(f"CV file not found: {cv_path}")
    if (out_dir / DEFAULT_FILES["profile"]).exists():
        if args.force:
            backup_existing(out_dir)
        elif args.merge:
            todo("merge mode")
        else:
            die(f"{DEFAULT_FILES['profile']} already exists. Use --force or --merge.")

    # Step 1: convert CV to text
    cv_txt = extract_text_from_cv(cv_path)
    txt_path = out_dir / ".aris-homepage" / "cv.txt"
    txt_path.parent.mkdir(parents=True, exist_ok=True)
    txt_path.write_text(cv_txt, encoding="utf-8")

    # Step 2: LLM extraction handoff
    #   Print instructions for the calling Claude agent to read cv.txt, fill the schema,
    #   and write the resulting JSON to .aris-homepage/extraction.json.
    print_extraction_handoff(txt_path, out_dir)
    return 0


def extract_text_from_cv(path: Path) -> str:
    """Convert CV file → plain text. macOS textutil → cat → pdftotext fallback chain."""
    suffix = path.suffix.lower()
    if suffix == ".txt":
        return path.read_text(encoding="utf-8")
    if suffix == ".docx":
        # macOS textutil — universally available, zero pip deps
        if shutil.which("textutil"):
            result = subprocess.run(
                ["textutil", "-convert", "txt", "-stdout", str(path)],
                capture_output=True, text=True, check=True,
            )
            return result.stdout
        # python-docx fallback (optional pip install)
        try:
            import docx  # type: ignore
            doc = docx.Document(str(path))
            return "\n".join(p.text for p in doc.paragraphs)
        except ImportError:
            die("Cannot read .docx: install python-docx OR run on macOS (textutil).")
    if suffix == ".pdf":
        if shutil.which("pdftotext"):
            result = subprocess.run(
                ["pdftotext", str(path), "-"],
                capture_output=True, text=True, check=True,
            )
            return result.stdout
        die("Cannot read .pdf: install poppler-utils (provides pdftotext).")
    die(f"Unsupported CV format: {suffix}. Use .txt, .docx, or .pdf.")


def print_extraction_handoff(txt_path: Path, out_dir: Path) -> None:
    """Print the JSON schema + handoff instructions for the calling LLM agent."""
    # TODO: emit the JSON schema (constrained output spec)
    # TODO: emit the prompt template the agent should use
    # TODO: emit the expected output path .aris-homepage/extraction.json
    raise NotImplementedError("Extraction handoff — implement in next iteration")


# ---------------------------------------------------------------------------
# Command: render --persona
# ---------------------------------------------------------------------------

def cmd_render(args: argparse.Namespace) -> int:
    """Render homepage HTML from profile.yml + publications.bib + bio.md + news.md.

    Runs fact-check at the same time. Produces:
      - <out>.html
      - audit-report.md (next to the HTML)

    Hard-fail verdict blocks ship; --override-all bypasses with loud logging.
    """
    if args.persona not in PERSONAS:
        die(f"Unknown persona: {args.persona}. Choose from {PERSONAS}.")
    if args.persona == "active-researcher":
        die("active-researcher template is v1.1; only theory-minimal is shipping in v1.")

    workspace = Path(".").resolve()
    profile = load_profile(workspace / DEFAULT_FILES["profile"])
    bib = parse_bibtex(workspace / DEFAULT_FILES["bib"])
    bio_md = read_optional(workspace / DEFAULT_FILES["bio"])
    news_md = read_optional(workspace / DEFAULT_FILES["news"])

    # Fact-check phase (unless skipped)
    if not args.no_audit:
        audit = run_fact_check(profile, bib, override_all=args.override_all)
        write_audit_report(workspace / DEFAULT_FILES["audit_report"], audit)
        if audit.verdict == "BLOCKED" and not args.override_all:
            die(f"Audit BLOCKED. See {DEFAULT_FILES['audit_report']}. "
                f"Fix the issues OR re-run with --override-all (logged loudly).")

    # Render phase
    chunks = build_section_chunks(profile, bib, bio_md, news_md, persona=args.persona)
    template = (TEMPLATES_DIR / f"homepage-{args.persona}.html").read_text(encoding="utf-8")
    html = render_template(template, chunks, profile)
    out_path = Path(args.out) if args.out else workspace / DEFAULT_FILES["output_html"]
    out_path.write_text(html, encoding="utf-8")
    print(f"✓ Rendered {out_path}")
    return 0


def load_profile(path: Path) -> dict[str, Any]:
    """Load profile.yml. TODO: schema validation (schema_version check, required fields)."""
    if not HAS_YAML:
        die("pyyaml not installed. Run: pip install pyyaml")
    if not path.exists():
        die(f"{path} not found. Run `aris-homepage init --from-cv <cv>` first.")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    # TODO: validate schema_version == SCHEMA_VERSION
    # TODO: validate required fields (identity.name, affiliations.current)
    return data


def parse_bibtex(path: Path) -> dict[str, dict[str, Any]]:
    """Load publications.bib → {bibkey: entry_dict}. TODO: handle equal contribution markers."""
    if not HAS_BIBTEXPARSER:
        die("bibtexparser not installed. Run: pip install bibtexparser")
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        db = bibtexparser.load(f)
    return {entry["ID"]: entry for entry in db.entries}


def read_optional(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


# ---------------------------------------------------------------------------
# Fact-check
# ---------------------------------------------------------------------------

class AuditResult:
    """Aggregated audit outcome from fact-check phase."""
    def __init__(self) -> None:
        self.passed: list[dict] = []
        self.warned: list[dict] = []
        self.failed: list[dict] = []
        self.overridden: list[dict] = []

    @property
    def verdict(self) -> str:
        if self.failed:
            return "BLOCKED"
        if self.warned:
            return "WARN"
        return "PASS"


def run_fact_check(profile: dict, bib: dict, *, override_all: bool = False) -> AuditResult:
    """Run hard-fail + soft-warn checks against DBLP/arXiv. See SKILL.md for criteria."""
    result = AuditResult()
    overrides = profile.get("audit", {}).get("overrides", {})

    # Check 1: bibkey existence
    pubs_meta = profile.get("publications_meta", {})
    selected = profile.get("selected_publications", [])
    for key in selected:
        if key not in bib:
            result.failed.append({"key": key, "reason": "bibkey not found in publications.bib"})

    # Check 2-N: DBLP verification per selected paper
    for key in selected:
        if key not in bib:
            continue
        # Apply override
        if override_check(overrides.get(key, {}), key, result):
            continue
        # TODO: dblp_search_title(bib[key]["title"]) → compare venue/year/authors
        # TODO: arxiv fallback when DBLP empty
        # TODO: soft-warn on ambiguous matches
        pass

    # TODO: profile.identity vs profile.affiliations vs CV consistency cross-checks
    # TODO: award badge URL verification
    # TODO: forthcoming/future date sanity check

    if override_all:
        # Promote any remaining failures to overridden (loudly logged)
        result.overridden.extend(result.failed)
        result.failed = []

    return result


def override_check(override: dict, key: str, result: AuditResult) -> bool:
    """Returns True if override is valid + active; logs override for audit-report."""
    if not override:
        return False
    expires = override.get("expires")
    if expires:
        if datetime.now(timezone.utc).date().isoformat() > expires:
            result.failed.append({"key": key, "reason": f"override expired ({expires})"})
            return False
    result.overridden.append({"key": key, "fields": list(override.keys()),
                               "reason": override.get("reason", "no reason given")})
    return True


def dblp_search_title(title: str) -> list[dict]:
    """Search DBLP by title. Returns hit list or empty list."""
    q = urllib.parse.urlencode({"q": title, "format": "json", "h": 5})
    try:
        with urllib.request.urlopen(f"{DBLP_API}?{q}", timeout=15) as r:
            data = json.load(r)
        hits = data.get("result", {}).get("hits", {}).get("hit", [])
        return hits if isinstance(hits, list) else [hits]
    except Exception as e:
        print(f"  ⚠️ DBLP query failed for '{title[:60]}...': {e}", file=sys.stderr)
        return []


def write_audit_report(path: Path, audit: AuditResult) -> None:
    """Write Markdown audit report next to HTML. See SKILL.md for format."""
    # TODO: implement Markdown report writer matching the format in SKILL.md
    raise NotImplementedError("audit-report writer — implement in next iteration")


# ---------------------------------------------------------------------------
# Section chunk builders (Python builds HTML, template is just shell)
# ---------------------------------------------------------------------------

def build_section_chunks(profile: dict, bib: dict, bio_md: str, news_md: str,
                          *, persona: str) -> dict[str, str]:
    """Build per-section HTML chunks for {{PLACEHOLDER}} substitution.

    Empty sections degrade to empty string → section disappears from rendered page
    (no LLM filler, per gemini's risk #3).
    """
    return {
        "PHOTO_HTML": build_photo_html(profile),
        "PERSON_NAME": esc(profile["identity"]["name"]),
        "PERSON_NAME_NATIVE_HTML": build_native_name_html(profile),
        "TITLE_AFFILIATION_HTML": build_title_affil_html(profile),
        "EMAIL_HTML": build_email_html(profile),
        "SOCIAL_LINKS_HTML": build_social_html(profile),
        "BIO_SECTION_HTML": build_bio_section(profile, bio_md),
        "RESEARCH_SECTION_HTML": build_research_section(profile),
        "EDUCATION_SECTION_HTML": build_education_section(profile),
        "PUBLICATIONS_SECTION_HTML": build_publications_section(profile, bib, persona),
        "NEWS_SECTION_HTML": build_news_section(news_md),
        "AWARDS_SECTION_HTML": build_awards_section(profile),
        "TALKS_SECTION_HTML": build_talks_section(profile),
        "TEACHING_SECTION_HTML": build_teaching_section(profile),
        "AUDIT_LINK_HTML": f" · <a href=\"{DEFAULT_FILES['audit_report']}\">audit</a>",
    }


# Per-section builders — to be implemented in next iteration.
# Each returns "" when the corresponding profile.yml field is empty (graceful degradation).
def build_photo_html(p): return todo_stub("photo")
def build_native_name_html(p): return todo_stub("native_name")
def build_title_affil_html(p): return todo_stub("title_affil")
def build_email_html(p): return todo_stub("email")
def build_social_html(p): return todo_stub("social_links")
def build_bio_section(p, md): return todo_stub("bio")
def build_research_section(p): return todo_stub("research")
def build_education_section(p): return todo_stub("education")
def build_publications_section(p, bib, persona): return todo_stub("publications")
def build_news_section(md): return todo_stub("news")
def build_awards_section(p): return todo_stub("awards")
def build_talks_section(p): return todo_stub("talks")
def build_teaching_section(p): return todo_stub("teaching")


def render_template(template: str, chunks: dict[str, str], profile: dict) -> str:
    """Simple {{PLACEHOLDER}} substitution. Drift-detection meta included."""
    now = datetime.now(timezone.utc)
    base_vars = {
        "LANG": profile.get("ship", {}).get("lang", "en"),
        "PAGE_TITLE": f"{profile['identity']['name']} — Homepage",
        "SOURCE_PATH": DEFAULT_FILES["profile"],
        "SOURCE_SHA256": file_sha256(Path(DEFAULT_FILES["profile"])),
        "GENERATED_AT": now.isoformat(),
        "GENERATED_AT_DISPLAY": now.strftime("%Y-%m-%d"),
        "ACCENT_COLOR": profile.get("ship", {}).get("accent_color", "#1a4a8c"),
        "HEAD_CDN": "",  # TODO: optional MathJax CDN
        "AUDIT_VERDICT": "TODO",  # TODO: thread audit result into here
    }
    base_vars.update(chunks)
    html = template
    for k, v in base_vars.items():
        html = html.replace("{{" + k + "}}", v if v is not None else "")
    return html


# ---------------------------------------------------------------------------
# Command: check (audit only, no render)
# ---------------------------------------------------------------------------

def cmd_check(args: argparse.Namespace) -> int:
    """Run fact-check without rendering. Updates audit-report.md only."""
    workspace = Path(".").resolve()
    profile = load_profile(workspace / DEFAULT_FILES["profile"])
    bib = parse_bibtex(workspace / DEFAULT_FILES["bib"])
    audit = run_fact_check(profile, bib)
    write_audit_report(workspace / DEFAULT_FILES["audit_report"], audit)
    print(f"Audit: {audit.verdict}  (PASS {len(audit.passed)} · WARN {len(audit.warned)} · "
          f"FAIL {len(audit.failed)} · OVERRIDDEN {len(audit.overridden)})")
    if args.strict and audit.warned:
        return 1
    return 0 if audit.verdict != "BLOCKED" else 1


# ---------------------------------------------------------------------------
# Command: doctor
# ---------------------------------------------------------------------------

def cmd_doctor(args: argparse.Namespace) -> int:
    """Diagnostic: Python, deps, textutil/pdftotext, DBLP reachability."""
    print("ARIS Homepage Doctor")
    print(f"  Python:        {sys.version.split()[0]}")
    print(f"  pyyaml:        {'✓' if HAS_YAML else '✗  (pip install pyyaml)'}")
    print(f"  bibtexparser:  {'✓' if HAS_BIBTEXPARSER else '✗  (pip install bibtexparser)'}")
    print(f"  textutil:      {'✓' if shutil.which('textutil') else '✗  (macOS only)'}")
    print(f"  pdftotext:     {'✓' if shutil.which('pdftotext') else '✗  (brew install poppler)'}")
    print(f"  templates dir: {'✓' if TEMPLATES_DIR.exists() else '✗ ' + str(TEMPLATES_DIR)}")
    print("  DBLP reachable: ", end="", flush=True)
    try:
        with urllib.request.urlopen("https://dblp.org/", timeout=5) as r:
            print("✓" if r.status == 200 else f"⚠️ HTTP {r.status}")
    except Exception as e:
        print(f"✗  ({e})")
    return 0


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def esc(s: str) -> str:
    """HTML-escape user-supplied text. Reuses render_html.py for parity."""
    import html
    return html.escape(s, quote=True)


def file_sha256(path: Path) -> str:
    if not path.exists():
        return "missing"
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def backup_existing(out_dir: Path) -> None:
    """Backup existing artifacts to *.bak-TIMESTAMP before overwriting."""
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    for key in ("profile", "bib", "bio", "news", "extraction_review"):
        f = out_dir / DEFAULT_FILES[key]
        if f.exists():
            f.rename(f.with_suffix(f.suffix + f".bak-{ts}"))


def die(msg: str) -> None:
    print(f"✗ {msg}", file=sys.stderr)
    sys.exit(1)


def todo(what: str) -> None:
    print(f"TODO: {what} — not yet implemented", file=sys.stderr)
    sys.exit(2)


def todo_stub(name: str) -> str:
    """Placeholder for section builders not yet implemented."""
    return f"<!-- TODO build {name} section -->"


# ---------------------------------------------------------------------------
# Main / argparse
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(
        prog="aris-homepage",
        description="Generate a fact-checked academic homepage from a CV.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="bootstrap workspace from CV")
    p_init.add_argument("--from-cv", required=True, help=".docx / .pdf / .txt CV path")
    p_init.add_argument("--out", default=".", help="output directory (default: cwd)")
    g = p_init.add_mutually_exclusive_group()
    g.add_argument("--force", action="store_true", help="overwrite existing profile.yml")
    g.add_argument("--merge", action="store_true", help="fill only missing fields")
    p_init.set_defaults(func=cmd_init)

    p_render = sub.add_parser("render", help="render homepage HTML (runs fact-check)")
    p_render.add_argument("--persona", default="theory-minimal", choices=PERSONAS)
    p_render.add_argument("--out", help="output HTML path (default: index.html)")
    p_render.add_argument("--override-all", action="store_true",
                          help="ship past hard-fail (loudly logged in audit-report)")
    p_render.add_argument("--no-audit", action="store_true", help="skip fact-check (fast iter)")
    p_render.add_argument("--offline", action="store_true", help="skip CDN refs")
    p_render.set_defaults(func=cmd_render)

    p_check = sub.add_parser("check", help="fact-check only, no render")
    p_check.add_argument("--strict", action="store_true", help="treat WARN as FAIL")
    p_check.set_defaults(func=cmd_check)

    p_doctor = sub.add_parser("doctor", help="environment + dependency diagnostic")
    p_doctor.set_defaults(func=cmd_doctor)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
