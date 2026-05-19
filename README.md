<p align="center">
  <img src="assets/aris_logo.svg" alt="ARIS — Auto Research in Sleep" width="640">
</p>

# ARIS in 秋招

> 希望大家秋招的时候轻松一点 🌱

中文 ML / LLM / 多模态 / 生成式面试 cheat sheet 合集，由 **[ARIS — Auto Research in Sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)** 的 `/render-html` workflow 自动生成。

每篇都是一份长文 + 公式 + 从零开始的 PyTorch 代码 + 25 高频面试题（L1 必会 · L2 进阶 · L3 顶级 lab）；HTML 渲染为 academic-newspaper 排版，sticky TOC + MathJax + 代码高亮，**手机和 iPad 上读都不糊**。

---

## 🌟 ARIS 是什么 — 顺便安利一下

[**ARIS — Auto Research in Sleep**](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) 是 2025-2026 年最受关注的 AI 科研 agent skill 平台之一。这个仓库生成所用的 `/interview-cheatsheet` + `/render-html` 是 ARIS 74+ 个 skill 中的两个。

[![Stars](https://img.shields.io/github/stars/wanshuiyin/Auto-claude-code-research-in-sleep?style=flat&logo=github&logoColor=white&color=gold&label=Stars)](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/stargazers) · [![arXiv](https://img.shields.io/badge/arXiv-2605.03042-b31b1b?style=flat&logo=arxiv)](https://huggingface.co/papers/2605.03042) · [![HF Daily #1](https://img.shields.io/badge/HF%20Daily%20Papers-%231-yellow?style=flat)](https://huggingface.co/papers/2605.03042) · [![PaperWeekly](https://img.shields.io/badge/Featured%20on-PaperWeekly-red?style=flat)](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) · [![awesome-agent-skills](https://img.shields.io/badge/Featured%20in-awesome--agent--skills-blue?style=flat&logo=github)](https://github.com/VoltAgent/awesome-agent-skills) · [![Project of the Day](https://img.shields.io/badge/AI%20Digital%20Crew-Project%20of%20the%20Day-orange?style=flat)](https://aidigitalcrew.com)

- ⭐ **~10k GitHub stars** — top trending AI agent repo
- 🥇 **HuggingFace Daily Papers #1** — top of the day, paper [arXiv:2605.03042](https://huggingface.co/papers/2605.03042)
- 🏆 **AI Digital Crew · Project of the Day** (2026.03.14)
- 📰 **Featured on PaperWeekly** + **VoltAgent/awesome-agent-skills**
- 🛠️ **74+ research skills** — 从找 idea → 跑实验 → 写论文 → rebuttal → 做 talk slides 的全流程
- 🌐 **7+ 平台支持** — Claude Code · Codex CLI · Cursor · Trae · Antigravity · GitHub Copilot CLI · OpenClaw
- 🔧 **ARIS-Code 独立 CLI** — 不想绑定 Claude Code 也行，自带 multi-provider runtime

核心方法论：**跨模型对抗审查**——executor 和 reviewer 必须不同模型家族（Claude × GPT-5.5 xhigh × Gemini），不让 LLM 自己审自己。这套协议复用到面试 cheat sheet 生成上，就保证了每篇里的公式 / 代码 / 引用都过了一遍独立审查（详见每篇旁边的 `.review.json` 审计 trail）。

👉 **ARIS 主仓库**：https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep

---

## 📚 教程清单

### 🧠 General / 基础

| Topic | HTML（推荐阅读） | Source MD |
|---|---|---|
| **Attention 面试 Cheat Sheet** | [📄 HTML](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/attention_tutorial.html) | [MD](docs/tutorials/attention_tutorial.md) |

### 🎯 Post-Training & Reasoning

| Topic | HTML | MD |
|---|---|---|
| RLHF / DPO / GRPO / PPO | 🚧 | — |
| Reasoning Models (o1 / R1 / Test-Time Compute / PRM) | 🚧 | — |

### 🏛️ LLM Architecture & Systems

| Topic | HTML | MD |
|---|---|---|
| MoE (DeepSeek-V3 / Mixtral / Llama 4) | 🚧 | — |
| Long Context (RoPE / YaRN / NTK / MLA / StreamingLLM) | 🚧 | — |
| KV Cache + Speculative Decoding (Medusa / EAGLE / MLA) | 🚧 | — |
| Quantization (GPTQ / AWQ / FP8 / NVFP4 / SmoothQuant) | 🚧 | — |
| Distributed Training (DDP / FSDP2 / ZeRO / TP / PP / EP / SP) | 🚧 | — |

### 🌊 Generative Models — 理论 & Tokenizers

| Topic | HTML | MD |
|---|---|---|
| **Flow Matching Quick Reference** | [📄 HTML](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/flow_matching_tutorial.html) | [MD](docs/tutorials/flow_matching_tutorial.md) |
| Diffusion Foundations (DDPM / Score / DDIM / EDM / CFG) | 🚧 | — |
| VAE / VQ-VAE / VQ-GAN / FSQ | 🚧 | — |

### 🎨 Generation Systems — 图像 / 视频 / 3D

| Topic | HTML | MD |
|---|---|---|
| Image Gen Systems (LDM / SD / SDXL / SD3 / FLUX / ControlNet) | 🚧 | — |
| Video Gen (Sora / Hunyuan-Video / Kling / Wan / Movie Gen) | 🚧 | — |
| 3D Gen (NeRF / Instant-NGP / 3DGS / SDS / Trellis) | 🚧 | — |

### 👁️ Multimodal

| Topic | HTML | MD |
|---|---|---|
| VLM (CLIP / LLaVA / Qwen-VL / DeepSeek-VL) | 🚧 | — |

> 🚧 表示正在跑（13 篇 background agent 进行中，跑完会逐个填入）。

---

## 🤖 这些教程是怎么生成的

每篇都用了 [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) 的 `/interview-cheatsheet` skill：

1. **Plan** — 12-14 节（TL;DR · 直觉 · 公式 · 代码 · 变体 · 复杂度 · 25 高频题）
2. **Draft** — ~600-1000 行中文 + 真能跑的 PyTorch
3. **Cross-model review** — 跨模型 codex GPT-5.5 xhigh 审 10 项（公式正确性 / 代码可运行 / 引用真实 / 表格 pipe 转义 / callout 风格 / 个人信息泄漏…）
4. **Fix 循环 ≤ 3 轮**
5. **`/render-html`** 渲染 + 13 项渲染审查（信息保真 / TOC / 公式 / 代码高亮 / 安全 / 隐私…）
6. **`.review.json`** 完整审计 trail

跨模型对抗审查（executor != reviewer 家族）是 ARIS 的核心不变量——LLM 自己审自己等于没审。

---

## License

[MIT](LICENSE) — 用、改、传、二开都行。希望对正在准备秋招的你有帮助。加油 💪

如果你写了新的 cheat sheet 想合并进来，欢迎 PR。
