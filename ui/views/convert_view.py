
import customtkinter as ctk
import threading
from tkinter import filedialog
import os
from core.converter import MediaConverter
from utils.config import CONVERT_CONFIG

class ConvertView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.input_file = None
        self.cancel_event = threading.Event()
        
        self.grid_columnconfigure(0, weight=1)
        # Row 5: Log Area (expand)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=0)

        self.build_ui()

    def build_ui(self):
        # Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="格式转换 (视频 -> 音频)", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # 1. File Selection
        self.file_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.file_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.file_frame.grid_columnconfigure(1, weight=1)

        self.file_btn = ctk.CTkButton(
            self.file_frame,
            text="选择视频文件",
            command=self.select_file,
            width=120,
            corner_radius=0
        )
        self.file_btn.grid(row=0, column=0, padx=(0, 10))

        self.file_label = ctk.CTkLabel(
            self.file_frame,
            text="未选择文件",
            text_color="gray",
            anchor="w"
        )
        self.file_label.grid(row=0, column=1, sticky="ew")

        # 2. Options
        self.options_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.options_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.format_label = ctk.CTkLabel(self.options_frame, text="输出格式:")
        self.format_label.grid(row=0, column=0, padx=(0, 10))
        
        self.format_menu = ctk.CTkOptionMenu(
            self.options_frame,
            values=CONVERT_CONFIG["supported_formats"],
            corner_radius=0
        )
        self.format_menu.set(CONVERT_CONFIG["default_format"])
        self.format_menu.grid(row=0, column=1, padx=(0, 20))

        self.bitrate_label = ctk.CTkLabel(self.options_frame, text="音频码率:")
        self.bitrate_label.grid(row=0, column=2, padx=(0, 10))
        
        self.bitrate_menu = ctk.CTkOptionMenu(
            self.options_frame,
            values=CONVERT_CONFIG["supported_bitrates"],
            corner_radius=0
        )
        self.bitrate_menu.set(CONVERT_CONFIG["default_bitrate"])
        self.bitrate_menu.grid(row=0, column=3)

        # 3. Action Buttons
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.grid(row=3, column=0, padx=20, pady=20)

        self.convert_btn = ctk.CTkButton(
            self.action_frame,
            text="开始转换",
            command=self.start_convert,
            state="disabled",
            height=40,
            font=ctk.CTkFont(size=16),
            corner_radius=0
        )
        self.convert_btn.grid(row=0, column=0, padx=(0, 10))

        self.stop_btn = ctk.CTkButton(
            self.action_frame,
            text="停止",
            command=self.stop_convert,
            state="disabled",
            height=40,
            fg_color="red",
            hover_color="darkred",
            font=ctk.CTkFont(size=16),
            corner_radius=0
        )
        self.stop_btn.grid(row=0, column=1, padx=(10, 0))

        # 4. Progress
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.progress_frame.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(self.progress_frame, text="")
        self.status_label.grid(row=0, column=0, pady=(0, 5))

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.grid(row=1, column=0, sticky="ew")
        self.progress_bar.set(0)
        self.progress_bar.grid_remove()

        # 5. Log Area (Optimized)
        self.log_frame = ctk.CTkFrame(self, fg_color=("gray90", "gray10")) # Darker background in dark mode
        self.log_frame.grid(row=5, column=0, padx=20, pady=(10, 20), sticky="nsew")
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

    def select_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Video Files", "*.mp4 *.mkv *.avi *.flv *.mov *.wmv")]
        )
        if filename:
            self.input_file = filename
            self.file_label.configure(text=os.path.basename(filename))
            self.convert_btn.configure(state="normal")

    def start_convert(self):
        if not self.input_file:
            return

        self.cancel_event.clear()
        self.convert_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress_bar.grid()
        self.progress_bar.set(0)
        self.status_label.configure(text="准备转换...", text_color=("gray10", "gray90"))

        threading.Thread(target=self._convert_task, daemon=True).start()

    def stop_convert(self):
        if self.cancel_event:
            self.cancel_event.set()
        self.stop_btn.configure(state="disabled")
        self.status_label.configure(text="正在停止...")

    def _update_progress(self, percent):
        self.after(0, self._update_progress_ui, percent)

    def _update_progress_ui(self, percent):
        self.progress_bar.set(percent / 100)
        self.status_label.configure(text=f"转换中: {percent:.1f}%")

    def _convert_task(self):
        output_format = self.format_menu.get()
        bitrate = self.bitrate_menu.get()
        
        self.log(f"开始转换: {self.input_file} -> {output_format}")
        
        result = MediaConverter.convert_to_audio(
            self.input_file,
            output_format,
            bitrate,
            self._update_progress,
            self.cancel_event
        )
        
        self.after(0, self._convert_done, result)

    def _convert_done(self, result):
        self.convert_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        
        if result["success"]:
            self.log(f"转换成功: {result['output_path']}")
            self.status_label.configure(text="转换完成")
            self.progress_bar.set(1)
        else:
            self.log(f"转换失败: {result['message']}")
            self.status_label.configure(text="转换失败", text_color="red")
