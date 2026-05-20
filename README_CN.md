<p align="center">
  <img src="assets/aris_logo.svg" alt="ARIS — Auto Research in Sleep" width="640">
</p>

# ARIS-in-AI-Offer (ARIS in 秋招)

> 希望大家秋招的时候轻松一点 🌱
>
> 📖 **English version (default)**: [README.md](README.md)

[![Stars](https://img.shields.io/github/stars/wanshuiyin/Auto-claude-code-research-in-sleep?style=flat&logo=github&logoColor=white&color=gold&label=ARIS%20Stars)](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/stargazers) · [![arXiv](https://img.shields.io/badge/arXiv-2605.03042-b31b1b?style=flat&logo=arxiv)](https://huggingface.co/papers/2605.03042) · [![HF Daily #1](https://img.shields.io/badge/HF%20Daily%20Papers-%231-yellow?style=flat)](https://huggingface.co/papers/2605.03042) · [![PaperWeekly](https://img.shields.io/badge/Featured%20on-PaperWeekly-red?style=flat)](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) · [![awesome-agent-skills](https://img.shields.io/badge/Featured%20in-awesome--agent--skills-blue?style=flat&logo=github)](https://github.com/VoltAgent/awesome-agent-skills) · [![Project of the Day](https://img.shields.io/badge/AI%20Digital%20Crew-Project%20of%20the%20Day-orange?style=flat)](https://aidigitalcrew.com)

> 🏆 **建立在已经验证的方法论上** —— [**ARIS 主仓**](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) 拿了 ~10k GitHub stars，HuggingFace Daily Papers #1，AI Digital Crew Project of the Day，74+ 个 research skill 跑在 7+ 平台上。这里不是 vaporware preview —— **每一篇 cheat sheet 都是同一个 `/interview-cheatsheet` + `/render-html` workflow 的产出**，跟科研生产里用的是同一套。

**双语**（中文 + English）ML / LLM / 多模态 / diffusion / agent / 生成式面试 cheat sheet 合集，由 **[ARIS — Auto Research in Sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)** 的 `/render-html` workflow 自动生成。

每篇都是一份长文 + 公式 + 从零开始的 PyTorch 代码 + 25 高频面试题（L1 必会 · L2 进阶 · L3 顶级 lab）。

<p align="center">
  <img src="assets/preview_strip.jpg" alt="ARIS-in-AI-Offer 预览 — 基础知识 + 面试题 + 实际代码，截自一篇代表性 cheat sheet" width="100%">
</p>

> 📖 **预览**（上图）：每个 pillar 一张截图，全部来自 [Diffusion Foundations 教程](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/diffusion_foundations_tutorial.html) —— ① **基础知识点**（公式推导 + 直觉 + TL;DR），② **面试题**（25 高频题分层 L1/L2/L3），③ **实际代码**（可跑的 PyTorch，含 CFG 训练 + DDIM 采样）。这个三柱结构在本仓库每篇 cheat sheet 里都一样。

### 📱 HTML 格式哪里都能读，清清楚楚

地铁上掏手机、咖啡馆开 iPad、图书馆开笔记本——同一个 HTML 链接打开都能读：

- 🧮 **MathJax** 渲染所有 LaTeX 公式（**不是截图**，可缩放、可复制、可选中）
- 💻 **highlight.js** 给 PyTorch 代码高亮上色
- 📐 **响应式排版** 自动适配窗口宽度，不糊不溢出
- 📑 **Sticky TOC** 长文里随时跳转章节
- 💾 **单文件 HTML**，下载就能离线读，不依赖任何后端

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

> 🌐 **双语版**：每一篇 cheat sheet 都同时提供中文（默认）和英文 HTML 版本——文件名 `*_tutorial.html`（中文）和 `*_tutorial_en.html`（英文），下方表格的 HTML 列直接给出对应链接。

### 🧠 General / 基础

| Topic | HTML 中文 | HTML EN | MD |
|---|---|---|---|
| **Attention 面试 Cheat Sheet** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/attention_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/attention_tutorial_en.html) | [MD](docs/tutorials/attention_tutorial.md) |
| **KL Divergence in RLHF (k1/k2/k3 · placement gradient bias)** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/kl_divergence_rlhf_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/kl_divergence_rlhf_tutorial_en.html) | [MD](docs/tutorials/kl_divergence_rlhf_tutorial.md) |

### 🎯 Post-Training & Reasoning

| Topic | HTML 中文 | HTML EN | MD |
|---|---|---|---|
| **RLHF / DPO / GRPO / PPO** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/rlhf_dpo_grpo_ppo_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/rlhf_dpo_grpo_ppo_tutorial_en.html) | [MD](docs/tutorials/rlhf_dpo_grpo_ppo_tutorial.md) |
| **Reasoning Models (o1 / R1 / Test-Time Compute / PRM)** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/reasoning_models_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/reasoning_models_tutorial_en.html) | [MD](docs/tutorials/reasoning_models_tutorial.md) |
| **LLM On-Policy Distillation (MiniLLM / GKD / Qwen3 / Tinker)** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/llm_opd_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/llm_opd_tutorial_en.html) | [MD](docs/tutorials/llm_opd_tutorial.md) |

### 🏛️ LLM Architecture & Systems

| Topic | HTML 中文 | HTML EN | MD |
|---|---|---|---|
| **MoE (DeepSeek-V3 / Mixtral / Llama 4)** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/moe_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/moe_tutorial_en.html) | [MD](docs/tutorials/moe_tutorial.md) |
| **Long Context (RoPE / YaRN / NTK / MLA / StreamingLLM)** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/long_context_rope_yarn_mla_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/long_context_rope_yarn_mla_tutorial_en.html) | [MD](docs/tutorials/long_context_rope_yarn_mla_tutorial.md) |
| **KV Cache + Speculative Decoding (Medusa / EAGLE / MLA)** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/kv_cache_speculative_decoding_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/kv_cache_speculative_decoding_tutorial_en.html) | [MD](docs/tutorials/kv_cache_speculative_decoding_tutorial.md) |
| **Quantization (GPTQ / AWQ / FP8 / NVFP4 / SmoothQuant)** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/quantization_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/quantization_tutorial_en.html) | [MD](docs/tutorials/quantization_tutorial.md) |
| **Distributed Training (DDP / FSDP2 / ZeRO / TP / PP / EP / SP)** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/distributed_training_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/distributed_training_tutorial_en.html) | [MD](docs/tutorials/distributed_training_tutorial.md) |

### 🌊 Generative Models — 理论 & Tokenizers

| Topic | HTML 中文 | HTML EN | MD |
|---|---|---|---|
| **Flow Matching Quick Reference** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/flow_matching_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/flow_matching_tutorial_en.html) | [MD](docs/tutorials/flow_matching_tutorial.md) |
| **Diffusion Foundations (DDPM / Score / DDIM / EDM / CFG)** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/diffusion_foundations_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/diffusion_foundations_tutorial_en.html) | [MD](docs/tutorials/diffusion_foundations_tutorial.md) |
| **VAE / VQ-VAE / VQ-GAN / FSQ** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/vae_vqvae_vqgan_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/vae_vqvae_vqgan_tutorial_en.html) | [MD](docs/tutorials/vae_vqvae_vqgan_tutorial.md) |

### 🎨 Generation Systems — 图像 / 视频 / 3D / Diffusion 后训练

| Topic | HTML 中文 | HTML EN | MD |
|---|---|---|---|
| **Image Gen Systems (LDM / SD / SDXL / SD3 / FLUX / ControlNet)** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/image_generation_systems_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/image_generation_systems_tutorial_en.html) | [MD](docs/tutorials/image_generation_systems_tutorial.md) |
| **Video Gen (Sora / Hunyuan-Video / Kling / Wan / Movie Gen)** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/video_generation_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/video_generation_tutorial_en.html) | [MD](docs/tutorials/video_generation_tutorial.md) |
| **3D Gen (NeRF / Instant-NGP / 3DGS / SDS / Trellis)** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/3d_generation_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/3d_generation_tutorial_en.html) | [MD](docs/tutorials/3d_generation_tutorial.md) |
| **Diffusion Post-Training (DDPO / DPOK / DRaFT / AlignProp / Diffusion-DPO / Flow-GRPO)** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/diffusion_post_training_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/diffusion_post_training_tutorial_en.html) | [MD](docs/tutorials/diffusion_post_training_tutorial.md) |
| **Diffusion / Flow Distillation (CM / iCT / sCM / CTM / LCM / DMD/DMD2 / ADD/LADD)** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/diffusion_distillation_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/diffusion_distillation_tutorial_en.html) | [MD](docs/tutorials/diffusion_distillation_tutorial.md) |

### 👁️ Multimodal

| Topic | HTML 中文 | HTML EN | MD |
|---|---|---|---|
| **VLM (CLIP / LLaVA / Qwen-VL / DeepSeek-VL)** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/vlm_multimodal_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/vlm_multimodal_tutorial_en.html) | [MD](docs/tutorials/vlm_multimodal_tutorial.md) |

### 🤖 Agents

| Topic | HTML 中文 | HTML EN | MD |
|---|---|---|---|
| **Agent Foundations (ReAct / MCP / A2A / SWE-bench / GAIA / OSWorld)** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/agent_foundations_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/agent_foundations_tutorial_en.html) | [MD](docs/tutorials/agent_foundations_tutorial.md) |
| **Agentic RL (AgentTuning / ToolRL / RAGEN / WebRL / SWE-RL / GRPO for tool use)** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/agentic_rl_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/agentic_rl_tutorial_en.html) | [MD](docs/tutorials/agentic_rl_tutorial.md) |
| **Multi-Agent & Long-Horizon (CAMEL / AutoGen / MetaGPT / MoA / Debate / MemGPT / LATS)** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/multi_agent_long_horizon_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/multi_agent_long_horizon_tutorial_en.html) | [MD](docs/tutorials/multi_agent_long_horizon_tutorial.md) |
| **Self-Evolving Agents (Ctx2Skill / Native Evolution / A²RD / Voyager / Reflexion / STaR)** | [📄 中](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/self_evolving_agents_tutorial.html) | [📄 EN](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/self_evolving_agents_tutorial_en.html) | [MD](docs/tutorials/self_evolving_agents_tutorial.md) |

> 🎉 **23 篇 cheat sheet 全部就位**（2026-05），每篇都有中文 + 英文双语版本，覆盖 General / Post-Training / Architecture / Generative / Multimodal / Agents / Diffusion 后训练 七大类。本轮新增 4 篇：KL Divergence in RLHF、LLM On-Policy Distillation、Diffusion Post-Training、Diffusion Distillation。后续 Flow-OPD / Audio Gen / 更新 SOTA 等会逐步加 —— **PR 欢迎**（详见 [CONTRIBUTING](CONTRIBUTING.md)）。

---

## 🤖 这些教程是怎么生成的

每篇都用了 [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) 的 `/interview-cheatsheet` skill：

1. **Plan** — 12-14 节（TL;DR · 直觉 · 公式 · 代码 · 变体 · 复杂度 · 25 高频题）
2. **Draft** — ~600-1000 行中文 + 真能跑的 PyTorch
3. **Cross-model review** — 跨模型 codex GPT-5.5 xhigh 审 10 项（公式正确性 / 代码可运行 / 引用真实 / 表格 pipe 转义 / callout 风格 / 个人信息泄漏…）
4. **Fix 循环**（trajectory-based，FAIL 集在收敛就继续，同一问题反复出现或 ~6 轮没收敛就停）
5. **`/render-html`** 渲染 + 13 项渲染审查（信息保真 / TOC / 公式 / 代码高亮 / 安全 / 隐私…）
6. **`.review.json`** 完整审计 trail

跨模型对抗审查（executor != reviewer 家族）是 ARIS 的核心不变量——LLM 自己审自己等于没审。

---

## 🚧 即将推出

- 🌐 **ARIS-Homepage** *(TODO)* —— 给秋招同学**自动生成个人主页**（学术主页 / 作品集），由跟这些 cheat sheet 同一套 `/render-html` workflow 驱动。输入 CV + 项目列表 + 论文 bibliography，输出单文件 HTML，随处可部署，MathJax + 响应式排版，发布前跨模型审一遍事实性 claim（论文 venue / 时间 / 模型名）。**适合**：博士 candidate 做学术主页 / 实习候选人做作品集 / 想要不打 Hugo & Jekyll & Webflow 直接出一个像样个人站的人。**想参与 API 设计的话来 [issue](https://github.com/wanshuiyin/ARIS-in-AI-Offer/issues/new) 一起讨论。**

---

## 🤝 欢迎贡献

一个人的力量有限，希望靠大家一起把这套教程做得更完善。

完整贡献指南见 [**CONTRIBUTING.md**](CONTRIBUTING.md)（[English](CONTRIBUTING.md) · [中文](CONTRIBUTING_CN.md)）—— 含 ARIS workflow 调用、严格风格指南（headings / math / tables / callouts / 个人信息 banlist）、PR checklist。

**TL;DR**：用 ARIS 的 [`/interview-cheatsheet`](skills/interview-cheatsheet/SKILL.md) + [`/render-html`](skills/render-html/SKILL.md) workflow 跑出来再提 PR；两个 skill 都内置跨模型 codex 5.5 xhigh 审查 gate（数学 / 代码 / 引用 / 渲染保真），过了就有质量底线。Skill 源码和 `tools/render_html.py` 都在这个仓库里，可以直接 fork。

**坦白说**：现有教程把 HTML 基础结构（公式 / 代码 / 表格 / callout / TOC / 响应式）做扎实了，但某些主题最前沿（2025 下半年才出的方法、某些细分领域最新论文）大概率没全覆盖。发现哪里过时或有错，PR / issue 都欢迎。

---

## 💬 社区

**与 [ARIS 主仓](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) 共享一个社区** —— 同一个微信群既讨论 ARIS skill workflow，也讨论这份秋招 cheat sheet 合集。进群可以讨论面试准备、提新的 cheat sheet 主题需求、或反馈勘误 / 贡献：

<p align="center">
  <img src="assets/wechat_group.jpg" alt="WeChat 群二维码（与 ARIS 主仓共享）" width="300">
</p>

---

## License

[MIT](LICENSE) — 用、改、传、二开都行。希望对正在准备秋招的你有帮助。加油 💪
