# OpenRouter 免费模型提取 & 批量测试工具
一个基于 **Tkinter** 的桌面小工具，用于从 OpenRouter 官方 API（`https://openrouter.ai/api/v1/models`）提取所有**免费模型**（ID 后缀带 `:free`），并支持一键批量测试模型可用性。全程通过 **SOCKS5 代理**访问，适合网络受限环境使用。
---
## ✨ 功能特性
- 🆓 **免费模型提取**：从官方 `api/v1/models` 接口拉取全部模型，自动过滤出 ID 以 `:free` 结尾的免费模型，与官网 [models?variant=free](https://openrouter.ai/models?variant=free) 页面结果一致
- 🔌 **SOCKS5 代理支持**：支持账号密码认证，使用 `socks5h://` 协议实现远程 DNS 解析，避免本地 DNS 污染
- 🧪 **批量可用性测试**：一键遍历全部免费模型，向每个模型发送测试消息，实时显示测试进度
- 📊 **结果标记**：测试结果直接标注在列表末尾（✅ 可用 / ❌ 失败 / ⏱️ 超时）
- 📋 **一键复制**：双击列表项或点击按钮即可复制模型 ID，方便粘贴到其他工具中使用
- 🧵 **多线程不卡界面**：网络请求全部在后台线程执行，界面保持流畅
---
## 🖥️ 界面预览

<img width="762" height="572" alt="image" src="https://github.com/user-attachments/assets/974a0894-eabe-4326-90a9-b3986da55b57" />

---
## 📋 环境要求
| 项目 | 要求 |
|------|------|
| Python | 3.7 及以上 |
| 操作系统 | Windows / macOS / Linux（Tkinter 跨平台） |
| 网络 | 需要可用的 SOCKS5 代理（用于访问 OpenRouter） |
| 账号 | OpenRouter 账号及 API Key |
---
### 1. 安装依赖
把“openrouter.ai model name extraction tool.py”下载到本地，直接运行，报错交给AI，它会帮你分析什么原因。
