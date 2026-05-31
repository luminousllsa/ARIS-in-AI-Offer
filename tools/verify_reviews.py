#!/usr/bin/env python3
"""verify_reviews.py — structural guard for the ARIS-in-AI-Offer review audit chain.

Every shippable academic-template HTML in this repo is supposed to be a *reviewed*
artifact: a fresh cross-model Codex thread audits it and leaves a sibling
``<name>.review.json`` recording the verdict + thread id, and the HTML embeds an
``aris:source-sha256`` of the Markdown it was rendered from. This script makes that
contract machine-checkable instead of trusting that an agent remembered to do it.

It exists because "a .review.json exists" is NOT the same as "this artifact is
gated": sidecars can be stale (source edited after review), structurally broken
(no thread id), carry a non-shippable verdict (DEFERRED / FAIL), or be missing
entirely (e.g. the English editions). This guard names each of those states.

Pure stdlib. No pip install. Run from the repo root:

    python3 tools/verify_reviews.py                 # bootstrap mode (default)
    python3 tools/verify_reviews.py --mode strict    # CI mode, once baseline is clean
    python3 tools/verify_reviews.py --json           # machine-readable report

Modes
-----
bootstrap (default)
    Fail (exit 1) only on HARD breakage of an artifact that *claims* to be
    shippable: unparseable sidecar, source file missing, a non-shippable verdict
    (FAIL / DEFERRED / REVIEW_UNAVAILABLE / ERROR) or a missing thread id, or a
    stale *HTML* (embedded hash != current source -> the page on disk no longer
    matches its source). Everything softer -- stale review, missing sidecar hash,
    no sidecar at all, unmanaged hand-authored HTML -- is reported as WARN and
    catalogued, so the guard runs green on day one while you work the backlog down.
strict
    Any non-OK artifact fails (exit 1). Switch to this in CI once the bootstrap
    backlog is cleared.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# --- status taxonomy --------------------------------------------------------
# severity: 0 = ok, 1 = warn (catalogued), 2 = hard (breaks a shippable claim)
OK = "OK"
HTML_STALE = "HTML_STALE"
HTML_HASH_MISSING = "HTML_HASH_MISSING"   # managed HTML lacks aris:source-sha256 (can't prove freshness)
SOURCE_MISSING = "SOURCE_MISSING"
JSON_UNPARSEABLE = "JSON_UNPARSEABLE"
REVIEW_INCOMPLETE = "REVIEW_INCOMPLETE"   # verdict FAIL/DEFERRED/REVIEW_UNAVAILABLE/ERROR or no thread id
REVIEW_STALE = "REVIEW_STALE"             # sidecar's recorded source hash != current source
SIDECAR_META_MISSING = "SIDECAR_META_MISSING"  # sidecar present but records no source hash
NO_THREAD_ID = "NO_THREAD_ID"             # shippable + fresh, but no codex thread id recorded
NO_SIDECAR = "NO_SIDECAR"                 # managed HTML (has aris:source meta) but no .review.json
UNMANAGED = "UNMANAGED"                   # HTML with no aris:source meta (not a render_html.py product)
EXEMPT = "EXEMPT"                         # an UNMANAGED artifact explicitly allowlisted (e.g. a hand-authored blog)

SEVERITY = {
    OK: 0,
    REVIEW_STALE: 1,
    SIDECAR_META_MISSING: 1,
    NO_THREAD_ID: 1,
    HTML_HASH_MISSING: 1,
    NO_SIDECAR: 1,
    UNMANAGED: 1,
    EXEMPT: 0,
    HTML_STALE: 2,
    SOURCE_MISSING: 2,
    JSON_UNPARSEABLE: 2,
    REVIEW_INCOMPLETE: 2,
}

# A verdict field is free-text in the wild (e.g. "PASS (WITH LENGTH WARN)",
# "FAIL_AT_ROUND_3_FIXED_POST_HOC"), so we judge by its LEADING token only.
# "PASS"/"WARN" ship; anything leading with FAIL/DEFERRED/ERROR/BLOCKED/REVIEW
# (or no verdict at all) is treated as not-cleanly-reviewed.
SHIPPABLE_TOKENS = {"PASS", "WARN"}

# Known limitations (this is a STRUCTURAL gate, not cryptographic attestation):
#  - It checks the HTML's recorded source hash against the current source, but does
#    NOT re-render and diff the HTML output, so a hand-edited HTML body whose source +
#    meta are untouched is not caught. (Output-hash diffing is the next hardening;
#    a plain re-render isn't byte-stable because of the embedded generation timestamp.)
#  - Sidecars are self-attesting: a PR editing both an artifact and its .review.json
#    can satisfy the structural checks. The backstop is human PR review + thread_ids
#    that trace to real Codex runs.
#
# Artifacts intentionally OUTSIDE the audited render pipeline (hand-authored, not
# a render_html.py product). An exemption can ONLY downgrade an UNMANAGED artifact
# to EXEMPT — it can NEVER mask a hard failure of a *managed* artifact (a broken
# tutorial still fails). Keep this list short, explicit, and reasoned; the report
# prints every exemption so it is never a silent bypass.
EXEMPTIONS = {
    "docs/blogs/continuous_dlm_2026h1_survey.html":
        "hand-authored long-form HTML, intentionally outside the audited /render-html "
        "pipeline (README states this); not a render_html.py product.",
}

META_RE = re.compile(
    r'<meta\s+name="(aris:[a-z0-9:_-]+)"\s+content="([^"]*)"\s*/?>',
    re.IGNORECASE,
)


@dataclass
class Record:
    html: str
    status: str = OK
    detail: str = ""
    source: str = ""
    sidecar: str = ""
    extra: dict = field(default_factory=dict)

    @property
    def severity(self) -> int:
        return SEVERITY.get(self.status, 2)


# --- helpers ----------------------------------------------------------------

def find_repo_root(start: Path) -> Path:
    """Walk up until we find a dir containing tools/render_html.py, else git root, else start."""
    cur = start.resolve()
    for cand in [cur, *cur.parents]:
        if (cand / "tools" / "render_html.py").is_file():
            return cand
    # fall back to git toplevel
    for cand in [cur, *cur.parents]:
        if (cand / ".git").exists():
            return cand
    return cur


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def parse_meta(html_text: str) -> dict:
    return {k.lower(): v for k, v in META_RE.findall(html_text)}


_LEAD_TOKEN_RE = re.compile(r"[A-Za-z]+")


def normalize_verdict(raw: str) -> str:
    """Free-text verdict -> leading UPPER token. 'PASS (WITH LENGTH WARN)' -> 'PASS',
    'FAIL_AT_ROUND_3_FIXED_POST_HOC' -> 'FAIL'."""
    m = _LEAD_TOKEN_RE.match((raw or "").strip())
    return m.group(0).upper() if m else ""


def gather_verdicts(sidecar: dict) -> dict:
    """Return {block_name: raw_verdict}. Schema B = math_code_review/render_review
    blocks; schema A (older render-only sidecars) = a single top-level 'verdict'."""
    out = {}
    for name in ("math_code_review", "render_review"):
        blk = sidecar.get(name)
        if isinstance(blk, dict) and blk.get("verdict"):
            out[name] = str(blk["verdict"])
    if not out and isinstance(sidecar.get("verdict"), str) and sidecar["verdict"].strip():
        out["review"] = sidecar["verdict"]
    return out


def _ids_from_block(block: dict) -> list[str]:
    ids = []
    for rnd in block.get("rounds", []) or []:
        tid = (rnd.get("thread_id") or "").strip()
        if tid:
            ids.append(tid)
    top = (block.get("thread_id") or "").strip()
    if top:
        ids.append(top)
    return ids


def collect_thread_ids_any(sidecar: dict) -> list[str]:
    """Scan both schemas for codex thread ids: review blocks' rounds, a top-level
    thread_id, and an older 'history' list of round records."""
    ids: list[str] = []
    for name in ("math_code_review", "render_review"):
        blk = sidecar.get(name)
        if isinstance(blk, dict):
            ids += _ids_from_block(blk)
    ids += _ids_from_block(sidecar)  # top-level thread_id / rounds
    for rec in sidecar.get("history", []) or []:
        if isinstance(rec, dict):
            tid = (rec.get("thread_id") or "").strip()
            if tid:
                ids.append(tid)
    return ids


def recorded_source_hash(sidecar: dict) -> str:
    """Return whatever source hash the sidecar recorded (full or 16-char prefix), or ''."""
    for key in ("source_sha256", "source_sha256_prefix"):
        v = sidecar.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip().lower()
    return ""


_HEX_RE = re.compile(r"^[0-9a-f]+$")


def hash_matches(recorded: str, current_full: str) -> bool:
    """Compare a recorded hash (full sha256 OR a >=12-char prefix) against the current
    full sha256. Both must be lowercase hex; current must be a full 64-char digest and
    the recorded prefix must be 12..64 chars. This rejects degenerate matches (a 1-char
    or over-length 'hash' that would slip through a naive min-length prefix compare)."""
    rec = (recorded or "").strip().lower()
    cur = (current_full or "").strip().lower()
    if not (_HEX_RE.match(rec) and _HEX_RE.match(cur)):
        return False
    if len(cur) != 64 or not (12 <= len(rec) <= 64):
        return False
    return cur.startswith(rec)


# --- core classification ----------------------------------------------------

def classify(html_path: Path, root: Path) -> Record:
    rel_html = html_path.relative_to(root).as_posix()
    text = html_path.read_text(encoding="utf-8", errors="replace")
    meta = parse_meta(text)

    src_rel = meta.get("aris:source-path", "")
    html_embedded_hash = meta.get("aris:source-sha256", "")

    if not src_rel:
        # An UNMANAGED artifact may be explicitly allowlisted (e.g. a hand-authored
        # blog). Exemption applies ONLY here — it can never reach a managed artifact's
        # hard failure below, so it cannot be used to hide a broken tutorial.
        # Governance guard: never honour an exemption for a render-product location
        # (docs/tutorials/*). Tutorials must ALWAYS be reviewed; refusing to exempt
        # them closes the "strip a tutorial's aris:source meta, then allowlist it" hole.
        if rel_html in EXEMPTIONS and not rel_html.startswith("docs/tutorials/"):
            return Record(html=rel_html, status=EXEMPT,
                          detail=f"exempt — {EXEMPTIONS[rel_html]}")
        return Record(html=rel_html, status=UNMANAGED,
                      detail="no aris:source-path meta — not a render_html.py product "
                             "(hand-authored HTML; outside the audited render pipeline)")

    source_path = (root / src_rel)
    rec = Record(html=rel_html, source=src_rel)

    if not source_path.is_file():
        rec.status = SOURCE_MISSING
        rec.detail = f"aris:source-path points at {src_rel} which does not exist"
        return rec

    current_hash = sha256_file(source_path)

    # 1) Is the HTML itself fresh vs its source? (needs re-render if not)
    if not html_embedded_hash:
        rec.status = HTML_HASH_MISSING
        rec.detail = "managed HTML has aris:source-path but no aris:source-sha256 — cannot prove the page matches its source"
        return rec
    if not hash_matches(html_embedded_hash, current_hash):
        rec.status = HTML_STALE
        rec.detail = (f"HTML embeds source hash {html_embedded_hash[:16]} but source is now "
                      f"{current_hash[:16]} — re-render this HTML")
        return rec

    # 2) Sidecar present?
    sidecar_path = html_path.with_suffix("").with_suffix(".review.json")
    # html_path like foo.html -> foo.review.json
    sidecar_path = html_path.parent / (html_path.name[:-len(".html")] + ".review.json")
    rec.sidecar = sidecar_path.relative_to(root).as_posix() if sidecar_path.exists() else ""
    if not sidecar_path.exists():
        rec.status = NO_SIDECAR
        rec.detail = "managed HTML (has aris:source meta) but no sibling .review.json"
        return rec

    # 3) Sidecar parseable?
    try:
        sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        rec.status = JSON_UNPARSEABLE
        rec.detail = f"sidecar unparseable: {e}"
        return rec

    # 4) Verdicts shippable? (handles both sidecar schemas; judged by leading token)
    verdicts = gather_verdicts(sidecar)
    if not verdicts:
        rec.status = REVIEW_INCOMPLETE
        rec.detail = "no verdict recorded (no math_code_review/render_review block and no top-level verdict)"
        return rec
    bad = [f"{name}={raw}" for name, raw in verdicts.items()
           if normalize_verdict(raw) not in SHIPPABLE_TOKENS]
    if bad:
        rec.status = REVIEW_INCOMPLETE
        rec.detail = "non-shippable verdict(s): " + "; ".join(bad)
        rec.extra["verdicts"] = bad
        return rec

    # 5) Review freshness: does the sidecar's recorded source hash match current source?
    recorded = recorded_source_hash(sidecar)
    if not recorded:
        rec.status = SIDECAR_META_MISSING
        rec.detail = "sidecar records no source_sha256 / source_sha256_prefix — cannot prove what was reviewed"
        return rec
    if not hash_matches(recorded, current_hash):
        rec.status = REVIEW_STALE
        rec.detail = (f"sidecar reviewed source @ {recorded[:16]} but source is now "
                      f"{current_hash[:16]} — content changed since review (needs delta re-review)")
        return rec

    # 6) Traceability: EVERY gating review block must carry its OWN codex thread id,
    #    so one block can't free-ride another block's traceability.
    missing_tid = []
    for name in verdicts:
        if name in ("math_code_review", "render_review"):
            if not _ids_from_block(sidecar.get(name, {})):
                missing_tid.append(name)
        else:  # schema A: single top-level verdict -> any top-level/rounds/history id
            if not collect_thread_ids_any(sidecar):
                missing_tid.append(name)
    if missing_tid:
        rec.status = NO_THREAD_ID
        rec.detail = "no codex thread_id for review block(s): " + ", ".join(missing_tid)
        return rec

    thread_ids = collect_thread_ids_any(sidecar)
    rec.status = OK
    rec.detail = f"reviewed (threads: {', '.join(sorted(set(thread_ids))[:3])}), hash fresh"
    return rec


def default_targets(root: Path) -> list[Path]:
    # Scan EVERY shippable HTML under docs/ recursively, so a new docs/ subdir can't
    # silently escape the gate. Per-artifact exemptions handle intentional exceptions.
    docs = root / "docs"
    return sorted(docs.rglob("*.html")) if docs.is_dir() else []


def main() -> int:
    ap = argparse.ArgumentParser(description="Structural guard for the ARIS review audit chain.")
    ap.add_argument("--mode", choices=["bootstrap", "strict"], default="bootstrap",
                    help="bootstrap (default): only hard breakage fails. strict: any non-OK fails.")
    ap.add_argument("--json", action="store_true", help="emit a machine-readable JSON report")
    ap.add_argument("paths", nargs="*", help="explicit HTML files to check (default: docs/tutorials, docs/blogs, docs/index.html)")
    args = ap.parse_args()

    root = find_repo_root(Path(__file__).parent)
    if args.paths:
        targets = [Path(p).resolve() for p in args.paths]
    else:
        targets = default_targets(root)

    records = [classify(p, root) for p in targets if p.is_file()]

    # group by status
    by_status: dict[str, list[Record]] = {}
    for r in records:
        by_status.setdefault(r.status, []).append(r)

    if args.json:
        payload = {
            "mode": args.mode,
            "total": len(records),
            "by_status": {s: len(v) for s, v in sorted(by_status.items())},
            "records": [
                {"html": r.html, "status": r.status, "detail": r.detail,
                 "source": r.source, "sidecar": r.sidecar, **({"extra": r.extra} if r.extra else {})}
                for r in records
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"ARIS review-chain guard — mode={args.mode}, {len(records)} HTML artifact(s)\n")
        order = sorted(by_status.keys(), key=lambda s: (-SEVERITY.get(s, 2), s))
        for status in order:
            recs = by_status[status]
            sev = SEVERITY.get(status, 2)
            tag = {0: "OK  ", 1: "WARN", 2: "FAIL"}[sev]
            print(f"[{tag}] {status} ({len(recs)})")
            for r in recs:
                line = f"    - {r.html}"
                if r.detail:
                    line += f"\n        {r.detail}"
                print(line)
            print()

    # exit policy
    hard = [r for r in records if r.severity == 2]
    warn = [r for r in records if r.severity == 1]
    if args.mode == "strict":
        failing = hard + warn
    else:
        failing = hard

    if not args.json:
        ok_n = len(by_status.get(OK, []))
        exempt_n = len(by_status.get(EXEMPT, []))
        exempt_str = f" · {exempt_n} EXEMPT" if exempt_n else ""
        print(f"summary: {ok_n} OK · {len(warn)} WARN · {len(hard)} FAIL{exempt_str}  "
              f"→ {'PASS' if not failing else 'BLOCK'} (mode={args.mode})")
        if args.mode == "bootstrap" and warn:
            print("  (bootstrap: WARN items are catalogued, not blocking — clear them, then switch to --mode strict)")

    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
