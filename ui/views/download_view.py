
import customtkinter as ctk
import threading
from tkinter import filedialog
import os
from core.downloader import VideoDownloader
from utils.config import PATHS

class DownloadView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.download_path = str(PATHS["downloads"])
        self.current_qualities = []
        self.cancel_event = threading.Event()
        
        # Grid layout configuration
        self.grid_columnconfigure(0, weight=1)
        # Row 0: Title
        # Row 1: URL Input
        # Row 2: Quality Dropdown
        # Row 3: Cookie & Path
        # Row 4: Action Buttons
        # Row 5: Progress
        # Row 6: Log Area (expand)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=0)

        self.build_ui()

    def build_ui(self):
        # Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="视频下载", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # 1. URL Input Area
        self.url_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.url_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.url_frame.grid_columnconfigure(0, weight=1)

        self.url_entry = ctk.CTkEntry(
            self.url_frame, 
            placeholder_text="请输入 Bilibili, YouTube 等视频链接",
            corner_radius=0
        )
        self.url_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.url_entry.bind("<Return>", lambda event: self.fetch_info())

        self.analyze_btn = ctk.CTkButton(
            self.url_frame, 
            text="获取信息", 
            command=self.fetch_info,
            width=100,
            corner_radius=0
        )
        self.analyze_btn.grid(row=0, column=1, sticky="e")

        # 2. Options Area
        self.quality_menu = ctk.CTkOptionMenu(
            self,
            values=["请先获取视频信息"],
            state="disabled",
            corner_radius=0
        )
        self.quality_menu.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # 3. Settings (Cookie & Path)
        self.settings_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.settings_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.settings_frame.grid_columnconfigure(1, weight=1)
        self.settings_frame.grid_columnconfigure(3, weight=1)

        # Cookie
        self.cookie_btn = ctk.CTkButton(
            self.settings_frame,
            text="导入 Cookie",
            command=self.select_cookie,
            width=100,
            corner_radius=0
        )
        self.cookie_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.cookie_label = ctk.CTkLabel(
            self.settings_frame,
            text="未选择 Cookie",
            text_color="gray",
            anchor="w"
        )
        self.cookie_label.grid(row=0, column=1, sticky="ew")

        # Path
        self.path_btn = ctk.CTkButton(
            self.settings_frame,
            text="选择保存路径",
            command=self.select_path,
            width=100,
            corner_radius=0
        )
        self.path_btn.grid(row=0, column=2, padx=(10, 10))
        
        self.path_label = ctk.CTkLabel(
            self.settings_frame,
            text=self.download_path,
            text_color="gray",
            anchor="w"
        )
        self.path_label.grid(row=0, column=3, sticky="ew")

        # 4. Action Buttons
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.grid(row=4, column=0, padx=20, pady=20)

        self.download_btn = ctk.CTkButton(
            self.action_frame,
            text="开始下载",
            command=self.start_download,
            state="disabled",
            height=40,
            font=ctk.CTkFont(size=16),
            corner_radius=0
        )
        self.download_btn.grid(row=0, column=0, padx=(0, 10))

        self.stop_btn = ctk.CTkButton(
            self.action_frame,
            text="停止",
            command=self.stop_download,
            state="disabled",
            height=40,
            fg_color="red",
            hover_color="darkred",
            font=ctk.CTkFont(size=16),
            corner_radius=0
        )
        self.stop_btn.grid(row=0, column=1, padx=(10, 0))

        # 5. Progress Area
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.progress_frame.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(self.progress_frame, text="")
        self.status_label.grid(row=0, column=0, pady=(0, 5))

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.grid(row=1, column=0, sticky="ew")
        self.progress_bar.set(0)
        self.progress_bar.grid_remove() # Hide initially

        # 6. Log Area (Optimized)
        self.log_frame = ctk.CTkFrame(self, fg_color=("gray90", "gray10")) # Darker background in dark mode
        self.log_frame.grid(row=6, column=0, padx=20, pady=(10, 20), sticky="nsew")
        self.log_frame.grid_columnconfigure(0, weight=1)
        self.log_frame.grid_rowconfigure(1, weight=1)

        self.log_header = ctk.CTkLabel(
            self.log_frame, 
            text=" 终端日志", 
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        self.log_header.grid(row=0, column=0, padx=5, pady=2, sticky="ew")

        self.log_textbox = ctk.CTkTextbox(
            self.log_frame, 
            state="disabled",
            font=ctk.CTkFont(family="Consolas", size=12), # Monospace font
            fg_color=("white", "black"),
            text_color=("black", "white"),
            activate_scrollbars=True
        )
        self.log_textbox.grid(row=1, column=0, padx=1, pady=1, sticky="nsew")

    def log(self, message):
        self.after(0, self._log_thread_safe, message)

    def _log_thread_safe(self, message):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"> {message}\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def select_cookie(self):
        filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if filename:
            self.cookie_label.configure(text=filename)

    def select_path(self):
        directory = filedialog.askdirectory()
        if directory:
            self.download_path = directory
            self.path_label.configure(text=directory)

    def fetch_info(self):
        url = self.url_entry.get()
        if not url:
            self.status_label.configure(text="请输入链接", text_color="red")
            return

        self.analyze_btn.configure(state="disabled")
        self.status_label.configure(text="正在获取视频信息...", text_color=("gray10", "gray90")) # reset color
        self.progress_bar.grid()
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()

        threading.Thread(target=self._fetch_info_task, args=(url,), daemon=True).start()

    def _fetch_info_task(self, url):
        cookie_file = self.cookie_label.cget("text")
        if "未选择" in cookie_file:
            cookie_file = None
            
        result = VideoDownloader.fetch_video_info(url, cookie_file)
        
        self.after(0, self._fetch_info_done, result)

    def _fetch_info_done(self, result):
        self.progress_bar.stop()
        self.progress_bar.grid_remove()
        self.analyze_btn.configure(state="normal")

        if result["success"]:
            self.current_qualities = result["qualities"]
            options = [q["display"] for q in self.current_qualities]
            # Default best option mapping logic
            # Since CTkOptionMenu displays text, we need to map display text back to ID when downloading
            self.quality_menu.configure(values=options, state="normal")
            if options:
                self.quality_menu.set(options[0])
            
            self.download_btn.configure(state="normal")
            self.log(f"获取成功: {result['title']}")
            self.status_label.configure(text=f"准备就绪: {result['title']}")
        else:
            self.log(f"获取失败: {result['error']}")
            self.status_label.configure(text="获取信息失败", text_color="red")

    def start_download(self):
        url = self.url_entry.get()
        selected_display = self.quality_menu.get()
        
        # Find quality ID
        quality_id = "best" # Default fallback
        for q in self.current_qualities:
            if q["display"] == selected_display:
                quality_id = q["id"]
                break
        
        cookie_file = self.cookie_label.cget("text")
        if "未选择" in cookie_file:
            cookie_file = None

        self.cancel_event.clear()
        self.download_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress_bar.grid()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(0)
        self.status_label.configure(text="准备下载...", text_color=("gray10", "gray90"))

        threading.Thread(
            target=self._download_task, 
            args=(url, quality_id, cookie_file), 
            daemon=True
        ).start()

    def stop_download(self):
        if self.cancel_event:
            self.cancel_event.set()
        self.stop_btn.configure(state="disabled")
        self.status_label.configure(text="正在停止...")

    def _update_progress(self, percent, speed):
        self.after(0, self._update_progress_ui, percent, speed)

    def _update_progress_ui(self, percent, speed):
        self.progress_bar.set(percent / 100)
        self.status_label.configure(text=f"下载中: {percent}% - {speed}")

    def _download_task(self, url, quality_id, cookie_file):
        self.log(f"开始下载: {url}")
        
        result = VideoDownloader.download_video(
            url, 
            self.download_path, 
            quality_id, 
            cookie_file, 
            self._update_progress,
            self.cancel_event
        )
        
        self.after(0, self._download_done, result)

    def _download_done(self, result):
        self.download_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        
        if result["success"]:
            self.log("下载完成!")
            self.status_label.configure(text="下载完成")
            self.progress_bar.set(1)
        else:
            self.log(f"下载出错: {result['message']}")
            self.status_label.configure(text="下载失败", text_color="red")
