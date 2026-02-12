
import customtkinter as ctk
import threading
from tkinter import filedialog
import os
from core.transcriber import VideoTranscriber
from utils.config import WHISPER_CONFIG
from ui.theme import Theme
import torch
import subprocess
import sys
import re

class TranscribeView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.input_file = None
        self.process = None
        
        self.grid_columnconfigure(0, weight=1)
        # 调整行权重，让日志区域 (Row 5) 占据剩余空间
        self.grid_rowconfigure(5, weight=1)

        self.build_ui()

    def build_ui(self):
        # Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="语音转文字 (Whisper)", 
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=24, weight="bold"),
            text_color=Theme.COLOR_TEXT_PRIMARY
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # 1. File Selection
        self.file_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.file_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.file_frame.grid_columnconfigure(1, weight=1)

        self.file_btn = ctk.CTkButton(
            self.file_frame,
            text="选择媒体文件",
            command=self.select_file,
            width=120,
            corner_radius=Theme.CORNER_RADIUS,
            fg_color=Theme.COLOR_SECONDARY,
            hover_color=Theme.COLOR_SECONDARY_HOVER,
            text_color=Theme.COLOR_TEXT_PRIMARY,
            border_width=Theme.BORDER_WIDTH,
            border_color=Theme.COLOR_BORDER,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY)
        )
        self.file_btn.grid(row=0, column=0, padx=(0, 10))

        self.file_label = ctk.CTkLabel(
            self.file_frame,
            text="未选择文件",
            text_color=Theme.COLOR_TEXT_SECONDARY,
            anchor="w",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY)
        )
        self.file_label.grid(row=0, column=1, sticky="ew")

        # 2. Options
        self.options_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.options_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        # Model Selection
        self.model_label = ctk.CTkLabel(self.options_frame, text="模型大小:", font=ctk.CTkFont(family=Theme.FONT_FAMILY))
        self.model_label.grid(row=0, column=0, padx=(0, 10))
        
        self.model_menu = ctk.CTkOptionMenu(
            self.options_frame,
            values=WHISPER_CONFIG["models"],
            corner_radius=Theme.CORNER_RADIUS,
            fg_color=Theme.COLOR_SECONDARY,
            button_color=Theme.COLOR_PRIMARY,
            button_hover_color=Theme.COLOR_PRIMARY_HOVER,
            text_color=Theme.COLOR_TEXT_PRIMARY,
            dropdown_fg_color=Theme.COLOR_SURFACE,
            dropdown_text_color=Theme.COLOR_TEXT_PRIMARY,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY)
        )
        self.model_menu.set(WHISPER_CONFIG["default_model"])
        self.model_menu.grid(row=0, column=1, padx=(0, 20))

        # Format Selection
        self.format_label = ctk.CTkLabel(self.options_frame, text="输出格式:", font=ctk.CTkFont(family=Theme.FONT_FAMILY))
        self.format_label.grid(row=0, column=2, padx=(0, 10))
        
        self.format_menu = ctk.CTkOptionMenu(
            self.options_frame,
            values=WHISPER_CONFIG["output_formats"],
            corner_radius=Theme.CORNER_RADIUS,
            fg_color=Theme.COLOR_SECONDARY,
            button_color=Theme.COLOR_PRIMARY,
            button_hover_color=Theme.COLOR_PRIMARY_HOVER,
            text_color=Theme.COLOR_TEXT_PRIMARY,
            dropdown_fg_color=Theme.COLOR_SURFACE,
            dropdown_text_color=Theme.COLOR_TEXT_PRIMARY,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY)
        )
        self.format_menu.set(WHISPER_CONFIG["default_format"])
        self.format_menu.grid(row=0, column=3, padx=(0, 20))

        # GPU Switch
        self.gpu_var = ctk.BooleanVar(value=torch.cuda.is_available())
        self.gpu_switch = ctk.CTkSwitch(
            self.options_frame,
            text="GPU加速",
            variable=self.gpu_var,
            onvalue=True,
            offvalue=False,
            state="normal" if torch.cuda.is_available() else "disabled",
            progress_color=Theme.COLOR_PRIMARY,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY)
        )
        self.gpu_switch.grid(row=0, column=4, padx=(0, 10))

        # Helper text
        self.helper_label = ctk.CTkLabel(
            self.options_frame, 
            text="注: 模型越大精度越高，但速度越慢。GPU加速需显卡支持。",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=12),
            text_color=Theme.COLOR_TEXT_SECONDARY
        )
        self.helper_label.grid(row=1, column=0, columnspan=5, pady=(5, 0), sticky="w")

        # 3. Action Buttons
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.grid(row=3, column=0, padx=20, pady=20)

        self.transcribe_btn = ctk.CTkButton(
            self.action_frame, 
            text="开始提取文字",
            command=self.start_transcribe,
            state="disabled",
            height=40,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=16),
            corner_radius=Theme.CORNER_RADIUS,
            fg_color=Theme.COLOR_PRIMARY,
            hover_color=Theme.COLOR_PRIMARY_HOVER,
            text_color=Theme.COLOR_TEXT_PRIMARY,
            text_color_disabled=Theme.COLOR_TEXT_SECONDARY
        )
        self.transcribe_btn.grid(row=0, column=0, padx=(0, 10))

        self.stop_btn = ctk.CTkButton(
            self.action_frame,
            text="停止",
            command=self.stop_transcribe,
            state="disabled",
            height=40,
            fg_color=Theme.COLOR_ERROR,
            hover_color="darkred",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=16),
            corner_radius=Theme.CORNER_RADIUS,
            text_color_disabled=Theme.COLOR_TEXT_SECONDARY
        )
        self.stop_btn.grid(row=0, column=1, padx=(10, 0))

        # 4. Progress Area (Optimized)
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.progress_frame.grid_columnconfigure(0, weight=1)

        # Info Row (Status + Percent)
        self.info_frame = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        self.info_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        self.info_frame.grid_columnconfigure(1, weight=1)

        self.status_label = ctk.CTkLabel(
            self.info_frame, 
            text="准备就绪", 
            anchor="w",
            text_color=Theme.COLOR_TEXT_SECONDARY,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY)
        )
        self.status_label.grid(row=0, column=0, sticky="w")

        self.percent_label = ctk.CTkLabel(
            self.info_frame, 
            text="", 
            anchor="e",
            text_color=Theme.COLOR_TEXT_PRIMARY,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, weight="bold")
        )
        self.percent_label.grid(row=0, column=1, sticky="e")

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame, 
            height=10,
            progress_color=Theme.COLOR_PRIMARY
        )
        self.progress_bar.grid(row=1, column=0, sticky="ew")
        self.progress_bar.set(0)
        self.progress_bar.grid_remove()

        # 5. Log Area (Optimized)
        self.log_frame = ctk.CTkFrame(self, fg_color=Theme.COLOR_SURFACE)
        self.log_frame.grid(row=5, column=0, padx=20, pady=(10, 20), sticky="nsew")
        self.log_frame.grid_columnconfigure(0, weight=1)
        self.log_frame.grid_rowconfigure(1, weight=1)

        self.log_header = ctk.CTkLabel(
            self.log_frame, 
            text=" 终端日志", 
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=12, weight="bold"),
            anchor="w",
            text_color=Theme.COLOR_TEXT_PRIMARY
        )
        self.log_header.grid(row=0, column=0, padx=5, pady=2, sticky="ew")

        self.log_textbox = ctk.CTkTextbox(
            self.log_frame, 
            state="disabled",
            font=ctk.CTkFont(family="Consolas", size=12), # Monospace font
            fg_color=Theme.COLOR_BG,
            text_color=Theme.COLOR_TEXT_PRIMARY,
            activate_scrollbars=True,
            corner_radius=Theme.CORNER_RADIUS
        )
        self.log_textbox.grid(row=1, column=0, padx=1, pady=1, sticky="nsew")

    def log(self, message):
        self.after(0, self._log_thread_safe, message)

    def _log_thread_safe(self, message):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"> {message}\n") # Add prefix
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def select_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Media Files", "*.mp4 *.mp3 *.wav *.m4a *.flac *.mkv")]
        )
        if filename:
            self.input_file = filename
            self.file_label.configure(text=os.path.basename(filename))
            self.transcribe_btn.configure(state="normal")

    def start_transcribe(self):
        if not self.input_file:
            return

        self.transcribe_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.gpu_switch.configure(state="disabled")
        self.progress_bar.grid()
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        
        self.status_label.configure(text="正在初始化...", text_color=("gray10", "gray90"))
        self.percent_label.configure(text="")

        threading.Thread(target=self._transcribe_task, daemon=True).start()

    def stop_transcribe(self):
        if self.process:
            try:
                self.process.terminate()
            except:
                pass
        self.stop_btn.configure(state="disabled")
        self.status_label.configure(text="正在停止...")

    def _update_progress(self, msg, percent):
        self.after(0, self._update_progress_ui, msg, percent)

    def _update_progress_ui(self, msg, percent):
        self.status_label.configure(text=msg)
        if percent > 0:
            self.progress_bar.configure(mode="determinate")
            self.progress_bar.set(percent / 100)
            self.percent_label.configure(text=f"{percent:.1f}%")
        else:
            self.progress_bar.configure(mode="indeterminate")
            self.progress_bar.start()
            self.percent_label.configure(text="")

    def _transcribe_task(self):
        model_name = self.model_menu.get()
        output_format = self.format_menu.get()
        use_gpu = self.gpu_switch.get() == 1
        
        script = """
import sys
from core.transcriber import VideoTranscriber
input_path = sys.argv[1]
model_name = sys.argv[2]
output_format = sys.argv[3]
use_gpu = sys.argv[4] == 'True'
VideoTranscriber.transcribe(input_path, model_name, output_format, use_gpu)
"""
        cmd = [sys.executable, "-c", script, self.input_file, model_name, output_format, str(use_gpu)]
        
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        try:
            self.process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True, 
                encoding='utf-8',
                startupinfo=startupinfo,
                errors='replace'
            )
        except Exception as e:
            self.after(0, self._transcribe_done, {"success": False, "message": str(e)})
            return
        
        duration = 0
        final_result = {"success": False, "message": "任务被终止或发生错误"}
        
        duration_pattern = re.compile(r"DURATION: ([\d\.]+)")
        # [00:00.000 --> 00:08.000] or [00:00:00.000 --> ...]
        timestamp_pattern = re.compile(r"--> (?:(\d{1,2}):)?(\d{2}):(\d{2})[\.,](\d{3})")
        result_pattern = re.compile(r"RESULT: (.+)")

        try:
            for line in self.process.stdout:
                line = line.strip()
                if not line: continue
                
                # Check Duration
                m_dur = duration_pattern.search(line)
                if m_dur:
                    duration = float(m_dur.group(1))
                    self._update_progress("正在转录...", 0)
                    continue
                
                # Check Result
                m_res = result_pattern.search(line)
                if m_res:
                    try:
                        final_result = eval(m_res.group(1))
                    except:
                        pass
                    continue

                # Check Timestamp
                m_time = timestamp_pattern.search(line)
                if m_time and duration > 0:
                    groups = m_time.groups()
                    # groups: (hours_str, mins_str, secs_str, ms_str)
                    h_str = groups[0]
                    m_str = groups[1]
                    s_str = groups[2]
                    ms_str = groups[3]
                    
                    h = int(h_str) if h_str else 0
                    m = int(m_str)
                    s = int(s_str)
                    ms = int(ms_str)
                    
                    seconds = h * 3600 + m * 60 + s + ms / 1000
                    percent = min(99, (seconds / duration) * 100)
                    self._update_progress(f"转录中: {percent:.1f}%", percent)
            
            self.process.wait()

        except Exception as e:
            final_result = {"success": False, "message": str(e)}
        finally:
            self.process = None

        self.after(0, self._transcribe_done, final_result)

    def _transcribe_done(self, result):
        self.progress_bar.stop()
        self.transcribe_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        if torch.cuda.is_available():
             self.gpu_switch.configure(state="normal")
        
        if result["success"]:
            self.log(f"✅ 成功: 输出至 {result['output_path']}")
            self.status_label.configure(text="提取完成")
            self.progress_bar.set(1)
            self.percent_label.configure(text="100%")
            self.progress_bar.configure(mode="determinate")
        else:
            self.log(f"❌ 失败: {result['message']}")
            self.status_label.configure(text="提取失败", text_color="red")
            self.percent_label.configure(text="")
