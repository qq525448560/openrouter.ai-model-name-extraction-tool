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
## 🚀 快速开始
### 1. 安装依赖
🚀 安装
前置要求
项目	要求	
Python	3.8+	
pip	最新版即可	
网络	能访问 PyPI 源（可用国内镜像）	
1. 克隆仓库
git clone https://github.com/你的用户名/你的仓库名.git
cd 你的仓库名
2. 安装依赖
项目根目录已包含 requirements.txt，一条命令装完：
pip install -r requirements.txt
requirements.txt 内容如下（随仓库一起提交，无需手动创建）：
requests>=2.31.0
pysocks>=1.7.1
说明：pysocks 是 requests 走 SOCKS5 代理的必需依赖，缺少它会在运行时报 Missing dependencies for SOCKS support。
3. 验证安装
python -c "import requests, socks; print('OK')"
输出 OK 即可运行主程序：
python free_model_tool.py
<details>
<summary><b>常见安装问题</b></summary>
pip 下载慢或超时
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
Linux 下报 No module named 'tkinter'
# Ubuntu / Debian
sudo apt install python3-tk
# Fedora
sudo dnf install python3-tkinter
找不到 pip 命令
python -m pip install -r requirements.txt
</details>
直接把上面这段替换掉 README 里原来的安装部分即可。核心改动是以 requirements.txt 为标准安装方式，这是 GitHub 开源 Python 项目的通用做法——用户 clone 下来一眼就知道怎么装，不用在 README 里抄命令。
**使用说明**：将以上内容保存为 `README.md`，与 Python 脚本放在同一目录即可。如果你的脚本文件名不是 `free_model_tool.py`，记得把 README 中的文件名替换为实际名称。
README 包含了：功能特性、环境要求、安装配置步骤、使用说明、免费模型机制解释（`:free` 后缀原理）、FAQ 排错指南和注意事项，可以直接用于 GitHub 仓库或本地说明文档。
