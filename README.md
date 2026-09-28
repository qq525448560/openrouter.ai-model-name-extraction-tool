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
┌──────────────────────────────────────────────────────────────────┐
│ OpenRouter 免费模型提取&批量测试工具（SOCKS5代理版）                  │
├──────────────────────────────────────────────────────────────────┤
│ [联网获取免费模型（:free后缀）] [一键批量测试全部模型可用性]           │
│ 双击列表项复制模型ID | 测试结果标记在末尾                            │
├──────────────────────────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────────────┐              │
│ │ deepseek/deepseek-chat-v3.1:free                 │              │
│ │ meta-llama/llama-3.3-70b-instruct:free           │              │
│ │ qwen/qwen3-coder:free                            │              │
│ │ google/gemma-3-27b-it:free                       │              │
│ │ ...                                               │              │
│ │ deepseek/deepseek-chat-v3.1:free | ✅ 可用        │              │
│ │ meta-llama/llama-3.3-70b-instruct:free | ⏱️ 超时  │              │
│ └──────────────────────────────────────────────────┘              │
├──────────────────────────────────────────────────────────────────┤
│ [复制选中模型ID]                                                   │
├──────────────────────────────────────────────────────────────────┤
│ ✅ 获取成功！免费模型（:free后缀）共 50 个                          │
└──────────────────────────────────────────────────────────────────┘
---
## 📋 环境要求
| 项目 | 要求 |
|------|------|
| Python | 3.7 及以上 |
| 操作系统 | Windows / macOS / Linux（Tkinter 跨平台） |
| 网络 | 需要可用的 SOCKS5 代理（用于访问 OpenRouter） |
| 账号 | OpenRouter 账号及 API Key |
---
## 🚀 快速开始
### 1. 安装依赖
```bash
# requests + PySocks（SOCKS5 代理必需）
pip install requests[socks]
⚠️ 注意：使用 SOCKS5 代理必须安装 PySocks，否则会报错
Missing dependencies for SOCKS support。
上面的 requests[socks] 会同时安装两者。
2. 获取 API Key
注册并登录 OpenRouter
进入 Keys 管理页面
点击 Create Key 创建一个新的 API Key
复制生成的 Key（以 sk-or- 开头）
3. 配置脚本
打开脚本，修改顶部配置区：
# ===================== 配置区 =====================
API_KEY = "sk-or-v1-你的API密钥"       # 替换为你的 OpenRouter API Key
PROXY_URL = "socks5h://用户名:密码@代理地址:端口"  # 替换为你的 SOCKS5 代理
# =================================================
4. 运行
python free_model_tool.py
⚙️ 配置详解
API_KEY
在 OpenRouter Keys 页面 创建，格式形如 sk-or-v1-...。
PROXY_URL（SOCKS5 代理）
支持三种写法：
# ① 带账号密码认证（推荐，socks5h = 远程DNS解析）
PROXY_URL = "socks5h://proxyuser:password@45.62.105.82:1080"
# ② 无认证
PROXY_URL = "socks5h://127.0.0.1:1080"
# ③ 本地代理（如 Clash / v2rayN 的默认端口）
PROXY_URL = "socks5h://127.0.0.1:7890"
💡 socks5 与 socks5h 的区别：
socks5:// —— 在本地解析域名，可能受 DNS 污染影响
socks5h:// —— 域名解析交给代理服务器完成，更抗污染，推荐使用
💡 不需要代理？ 如果你的网络可以直连 OpenRouter，可将 PROXY_URL 设为 None，并将代码中的 proxies 参数删除或设为 proxies=None。
📖 使用说明
① 获取免费模型列表
点击 「联网获取免费模型（:free后缀）」 按钮，工具会：
通过 SOCKS5 代理请求 https://openrouter.ai/api/v1/models
解析返回的 JSON，遍历全部模型
只保留 ID 以 :free 结尾的模型（如 qwen/qwen3-coder:free）
结果显示在列表中，状态栏显示模型总数
② 批量测试可用性
点击 「一键批量测试全部模型可用性」 按钮，工具会：
遍历列表中的每一个免费模型
向 https://openrouter.ai/api/v1/chat/completions 发送测试消息 "hello"（max_tokens=10）
根据返回结果标注状态：
标记	含义	
✅ 可用	返回 HTTP 200，模型可正常调用	
❌ 失败	请求被拒绝、模型下线或 Key 无权限	
⏱️ 超时	20 秒内无响应	
每个模型测试间隔 0.4 秒，避免触发速率限制
测试完成后，列表替换为「模型ID + 测试结果」格式
③ 复制模型 ID
双击列表中的任意一行 → 自动复制该模型 ID
选中一行后点击 「复制选中模型ID」 按钮 → 复制该模型 ID
即使该行带有 | ✅ 可用 等结果后缀，也会自动提取纯模型 ID（按 | 分割）
🆓 关于 OpenRouter 免费模型
:free 后缀是什么？
OpenRouter 上同一个模型可能有多个版本（变体），其中免费版会在 ID 末尾附加 :free，例如：
deepseek/deepseek-chat-v3.1          ← 付费版
deepseek/deepseek-chat-v3.1:free     ← 免费版 ✅
本工具的过滤逻辑就一行核心代码：
if mid.endswith(":free"):
    model_ids.append(mid)
这与官网筛选页 https://openrouter.ai/models?variant=free 展示的免费模型列表一致，但直接从 JSON API 获取，无需爬取网页。
免费模型的限制
限制项	说明	
每分钟请求数	免费模型总计约 20 次/分钟	
每日请求数	未充值账号约 50 次/天；充值 ≥ $10 后可提升至 1000 次/天	
并发	免费模型不允许并发请求	
上下文长度	部分免费版会缩减上下文窗口	
⚠️ 批量测试会快速消耗每日免费额度，请合理安排测试频率。
❓ 常见问题（FAQ）
<details>
<summary><b>Q1：点击获取后提示"请求失败"，怎么办？</b></summary>
按以下顺序排查：
代理是否可用：确认 SOCKS5 代理地址、端口、账号密码正确，代理服务正在运行
缺少 PySocks：执行 pip install requests[socks]
API Key 是否有效：去 Keys 页面 确认 Key 未被删除或禁用
看详细报错：弹窗中会显示具体错误信息（如 ProxyError、401 Unauthorized、SSLError 等），对症处理
</details>
<details>
<summary><b>Q2：为什么获取到的模型很少或为空？</b></summary>
OpenRouter 的免费模型列表是动态变化的，部分模型可能已下线
确认网络正常返回了完整 JSON（状态栏会显示获取到的数量）
稍后重试，或直接访问官网 free 页面对比确认
</details>
<details>
<summary><b>Q3：批量测试全部显示 ❌ 失败？</b></summary>
最常见原因是触发了免费额度限制（每日请求数用尽），或请求频率过高被限流。可尝试：
降低测试频率（增大代码中 time.sleep(0.4) 的数值）
第二天再测试
登录 OpenRouter 后台查看用量情况
</details>
<details>
<summary><b>Q4：不想用代理，能直连吗？</b></summary>
可以。将配置改为：
PROXY_URL = None
并将两处 proxies=proxies 参数改为 proxies=None（或直接删除该参数）。
</details>
<details>
<summary><b>Q5：测试结果里的 ⏱️ 超时是什么意思？</b></summary>
表示该模型在 20 秒（test_timeout）内没有返回响应。免费模型排队严重时很常见，可以在配置区将 self.test_timeout 调大后重测。
</details>
⚠️ 注意事项
保护 API Key：不要将填入真实 Key 的脚本分享给他人或上传到公开仓库
代理安全：示例中的代理地址和密码请替换为你自己的，用完及时更换
额度消耗：批量测试每个模型消耗 1 次请求，免费额度有限，请节制使用
模型时效性：OpenRouter 免费模型经常上下线，测试结果仅代表当前时刻状态
📁 项目结构
.
├── free_model_tool.py   # 主程序（单文件，开箱即用）
└── README.md            # 说明文档
📜 许可证
本项目仅供个人学习与研究使用，请遵守 OpenRouter 的服务条款。
使用本工具产生的一切后果（如额度消耗、账号限制等）由使用者自行承担。
---
**使用说明**：将以上内容保存为 `README.md`，与 Python 脚本放在同一目录即可。如果你的脚本文件名不是 `free_model_tool.py`，记得把 README 中的文件名替换为实际名称。
README 包含了：功能特性、环境要求、安装配置步骤、使用说明、免费模型机制解释（`:free` 后缀原理）、FAQ 排错指南和注意事项，可以直接用于 GitHub 仓库或本地说明文档。
