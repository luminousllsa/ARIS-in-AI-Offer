<p align="center">
  <img src="assets/aris_logo.svg" alt="ARIS — Auto Research in Sleep" width="640">
</p>

# ARIS in 秋招

> 希望大家秋招的时候轻松一点 🌱

中文 ML / LLM / 多模态 / 生成式面试 cheat sheet 合集，由 **[ARIS — Auto Research in Sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)** 的 `/render-html` workflow 自动生成。

每篇都是一份长文 + 公式 + 从零开始的 PyTorch 代码 + 25 高频面试题（L1 必会 · L2 进阶 · L3 顶级 lab）；HTML 渲染为 academic-newspaper 排版，sticky TOC + MathJax + 代码高亮，**手机和 iPad 上读都不糊**。

---

## 📚 教程清单

| Topic | HTML（推荐阅读） | Source MD |
|---|---|---|
| Attention 面试 Cheat Sheet | [📄 HTML](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/attention_tutorial.html) | [MD](docs/tutorials/attention_tutorial.md) |
| Flow Matching Quick Reference | [📄 HTML](https://wanshuiyin.github.io/ARIS-in-AI-Offer/tutorials/flow_matching_tutorial.html) | [MD](docs/tutorials/flow_matching_tutorial.md) |

> 🚧 **更多在路上** —— RLHF/DPO/GRPO · Reasoning Models (o1/R1) · MoE (DeepSeek-V3) · KV Cache + Speculative Decoding · Long Context (RoPE/YaRN/MLA) · Quantization (GPTQ/AWQ/FP8/NVFP4) · Distributed Training (FSDP2/ZeRO/TP/PP/EP) · Diffusion Foundations · VLM (CLIP/LLaVA/Qwen-VL) · VAE/VQ-VAE/VQ-GAN/FSQ · Image Gen (SD3/FLUX/ControlNet) · Video Gen (Sora/Hunyuan-Video/Wan) · 3D Gen (NeRF/3DGS/SDS) ... 还有 13 篇正在跑。

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

## 🔗 关于 ARIS

**ARIS = Auto Research in Sleep** — 一个让 Claude Code + Codex / Gemini 跨模型协同跑科研全流程的 skill 平台（找 idea → 跑实验 → 写论文 → 投稿 rebuttal → 做 talk slides）。74+ skill，2025-2026 年沉淀。

👉 https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep

这个仓库是 ARIS 在「秋招准备」场景下的一个用例 demo——同一套 `/render-html` 渲染管线、同一套跨模型审查协议，换个 prompt 就是 14 篇面试速查。

---

## License

[MIT](LICENSE) — 用、改、传、二开都行。希望对正在准备秋招的你有帮助。加油 💪

如果你写了新的 cheat sheet 想合并进来，欢迎 PR。
