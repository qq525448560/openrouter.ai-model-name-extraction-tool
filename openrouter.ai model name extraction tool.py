import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading
import time

# ===================== 配置区 =====================
API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# SOCKS5代理，使用 socks5h:// 远程DNS解析，去掉#后面的备注
# 需要下载   pip install requests[socks] 依赖
PROXY_URL = "socks5h://**:**@***.***.***.***:****"   #国内需要填写
# =================================================

class FreeModelTool:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenRouter 免费模型提取&批量测试工具")
        self.root.geometry("760x540")
        self.root.resizable(True, True)

        # API端点配置
        self.api_url_models = "https://openrouter.ai/api/v1/models"  # 官方API（全部模型）
        self.api_url_chat = "https://openrouter.ai/api/v1/chat/completions"
        # 网页参考URL（variant=free过滤的免费模型页面）
        self.web_free_url = "https://openrouter.ai/models?variant=free"
        
        self.test_prompt = "hello"
        self.test_timeout = 20

        # ========== 顶部操作区 ==========
        top_bar = ttk.Frame(root, padding=12)
        top_bar.pack(fill=tk.X)
        
        # 按钮1：从API端点获取全部模型（对应 api/v1/models）
        self.load_api_btn = ttk.Button(
            top_bar, text="加载API全部模型", command=self.load_api_models
        )
        self.load_api_btn.pack(side=tk.LEFT)
        
        # 按钮2：联网刷新免费模型（对应网页 variant=free）
        self.refresh_btn = ttk.Button(
            top_bar, text="刷新免费模型", command=self.refresh_free_list
        )
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        self.batch_test_btn = ttk.Button(
            top_bar, text="测试全部模型可用性", command=self.start_batch_test
        )
        self.batch_test_btn.pack(side=tk.LEFT, padx=5)
        ttk.Label(top_bar, text="双击列表项复制模型ID | 测试结果标记在末尾").pack(side=tk.LEFT)

        # ========== 模型列表区 ==========
        list_area = ttk.Frame(root, padding=(12, 0, 12, 12))
        list_area.pack(fill=tk.BOTH, expand=True)
        scroll = ttk.Scrollbar(list_area)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.model_listbox = tk.Listbox(
            list_area,
            yscrollcommand=scroll.set,
            font=("Consolas", 10),
            selectmode=tk.SINGLE,
            activestyle="dotbox"
        )
        self.model_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=self.model_listbox.yview)
        self.model_listbox.bind("<Double-Button-1>", lambda e: self.copy_current())

        # ========== 操作按钮区 ==========
        btn_bar = ttk.Frame(root, padding=(12, 0, 12, 12))
        btn_bar.pack(fill=tk.X)
        self.copy_btn = ttk.Button(
            btn_bar, text="复制选中模型ID", command=self.copy_current
        )
        self.copy_btn.pack(side=tk.LEFT)

        # ========== 底部状态栏 ==========
        self.status_text = tk.StringVar(
            value="就绪。可点击【加载API全部模型】或【联网刷新免费模型】"
        )
        status_bar = ttk.Label(
            root, textvariable=self.status_text, anchor=tk.W, padding=12
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.raw_model_list = []

    # ==================== 按钮1：从API获取全部模型 ====================
    def load_api_models(self):
        """从 https://openrouter.ai/api/v1/models 获取全部模型列表（不过滤）"""
        self._set_buttons_loading("正在从API获取全部模型列表...")
        threading.Thread(target=self._fetch_api_models, daemon=True).start()

    def _fetch_api_models(self):
        """从API端点获取全部模型（不进行免费过滤）"""
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        proxies = {
            "http": PROXY_URL,
            "https": PROXY_URL
        }
        try:
            resp = requests.get(
                self.api_url_models, 
                headers=headers, 
                timeout=30, 
                proxies=proxies
            )
            resp.raise_for_status()
            data = resp.json()
            
            # 获取全部模型ID（不进行免费过滤）
            model_ids = []
            for item in data.get("data", []):
                mid = item.get("id")
                if mid:
                    model_ids.append(mid)
            
            self.raw_model_list = model_ids
            self.root.after(0, self._render_list, model_ids, "API全部模型")
            
        except Exception as e:
            self.root.after(0, self._on_error, str(e))

    # ==================== 按钮2：联网刷新免费模型（variant=free） ====================
    def refresh_free_list(self):
        """联网获取免费模型列表（对应网页 https://openrouter.ai/models?variant=free）"""
        self._set_buttons_loading("正在获取免费模型列表（对应网页variant=free）...")
        threading.Thread(target=self._fetch_free_models, daemon=True).start()

    def _fetch_free_models(self):
        """从API获取数据并过滤出免费模型（匹配网页variant=free的结果）"""
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        proxies = {
            "http": PROXY_URL,
            "https": PROXY_URL
        }
        try:
            resp = requests.get(
                self.api_url_models, 
                headers=headers, 
                timeout=30, 
                proxies=proxies
            )
            resp.raise_for_status()
            data = resp.json()
            
            # 正确的免费模型过滤逻辑：
            # pricing.prompt == "0" 且 pricing.completion == "0"
            model_ids = []
            for item in data.get("data", []):
                pricing = item.get("pricing", {})
                # 免费模型：prompt和completion价格都为字符串"0"
                if (pricing.get("prompt") == "0" and 
                    pricing.get("completion") == "0"):
                    mid = item.get("id")
                    if mid:
                        model_ids.append(mid)
            
            self.raw_model_list = model_ids
            self.root.after(0, self._render_list, model_ids, "免费模型(variant=free)")
            
        except Exception as e:
            self.root.after(0, self._on_error, str(e))

    # ==================== 通用辅助方法 ====================
    def _set_buttons_loading(self, message):
        """设置按钮为加载中状态"""
        self.load_api_btn.config(state=tk.DISABLED)
        self.refresh_btn.config(state=tk.DISABLED)
        self.batch_test_btn.config(state=tk.DISABLED)
        self.status_text.set(message)

    def _render_list(self, models, source_name):
        """渲染模型列表到UI"""
        self.model_listbox.delete(0, tk.END)
        for name in models:
            self.model_listbox.insert(tk.END, name)
        count = len(models)
        if count > 0:
            self.status_text.set(
                f"✅ 获取成功！{source_name}共 {count} 个模型"
            )
        else:
            self.status_text.set(f"❌ 未获取到{source_name}模型")
        
        # 恢复按钮状态
        self.load_api_btn.config(state=tk.NORMAL)
        self.refresh_btn.config(state=tk.NORMAL)
        self.batch_test_btn.config(state=tk.NORMAL)

    def start_batch_test(self):
        """开始批量测试"""
        if len(self.raw_model_list) == 0:
            messagebox.showwarning("提示", "请先加载模型列表！")
            return
        
        self.load_api_btn.config(state=tk.DISABLED)
        self.refresh_btn.config(state=tk.DISABLED)
        self.batch_test_btn.config(state=tk.DISABLED)
        self.status_text.set("开始批量测试模型可用性（走SOCKS代理）...")
        threading.Thread(target=self._batch_test_thread, daemon=True).start()

    def _batch_test_thread(self):
        """批量测试线程"""
        result_list = []
        total = len(self.raw_model_list)
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        proxies = {
            "http": PROXY_URL,
            "https": PROXY_URL
        }

        for idx, model_id in enumerate(self.raw_model_list):
            self.root.after(0, lambda i=idx+1, t=total, m=model_id:
                           self.status_text.set(f"测试进度：{i}/{t} 当前模型：{m}"))
            payload = {
                "model": model_id,
                "messages": [{"role": "user", "content": self.test_prompt}],
                "max_tokens": 10
            }
            status = "❌ 失败"
            try:
                resp = requests.post(
                    self.api_url_chat, 
                    headers=headers, 
                    json=payload, 
                    timeout=self.test_timeout, 
                    proxies=proxies
                )
                if resp.status_code == 200:
                    status = "✅ 可用"
            except requests.exceptions.Timeout:
                status = "⏱️ 超时"
            except Exception as e:
                status = "❌ 失败"

            result_list.append(f"{model_id} | {status}")
            time.sleep(0.4)
        
        self.root.after(0, self._render_test_result, result_list)

    def _render_test_result(self, result_list):
        """渲染测试结果"""
        self.model_listbox.delete(0, tk.END)
        for line in result_list:
            self.model_listbox.insert(tk.END, line)
        self.status_text.set(f"批量测试完成！共 {len(result_list)} 个模型")
        
        # 恢复按钮状态
        self.load_api_btn.config(state=tk.NORMAL)
        self.refresh_btn.config(state=tk.NORMAL)
        self.batch_test_btn.config(state=tk.NORMAL)

    def _on_error(self, err_msg):
        """错误处理"""
        self.status_text.set(f"请求失败：{err_msg}")
        self.load_api_btn.config(state=tk.NORMAL)
        self.refresh_btn.config(state=tk.NORMAL)
        self.batch_test_btn.config(state=tk.NORMAL)
        messagebox.showerror("接口请求失败", f"详细信息：\n{err_msg}")

    def copy_current(self):
        """复制当前选中的模型ID"""
        selected = self.model_listbox.curselection()
        if not selected:
            messagebox.showwarning("提示", "请先在列表中选中一个模型")
            return
        full_text = self.model_listbox.get(selected[0])
        model_id = full_text.split(" | ")[0]
        self.root.clipboard_clear()
        self.root.clipboard_append(model_id)
        self.root.update()
        self.status_text.set(f"已复制模型ID：{model_id}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FreeModelTool(root)
    root.mainloop()
