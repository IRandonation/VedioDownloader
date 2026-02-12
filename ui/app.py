
import customtkinter as ctk
from utils.config import APP_NAME, UI_CONFIG
from ui.theme import Theme
from ui.views.download_view import DownloadView
from ui.views.convert_view import ConvertView
from ui.views.transcribe_view import TranscribeView

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title(APP_NAME)
        self.geometry(f"{UI_CONFIG['window_width']}x{UI_CONFIG['window_height']}")
        self.minsize(UI_CONFIG['min_width'], UI_CONFIG['min_height'])
        self.configure(fg_color=Theme.COLOR_BG)

        # Layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 1. Navigation Frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=Theme.COLOR_SURFACE)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_label = ctk.CTkLabel(
            self.navigation_frame, 
            text=APP_NAME,
            image=None, # Add logo here if available
            compound="left", 
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=15, weight="bold"),
            text_color=Theme.COLOR_TEXT_PRIMARY
        )
        self.navigation_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(
            self.navigation_frame, 
            corner_radius=Theme.CORNER_RADIUS, 
            height=40, 
            border_spacing=10, 
            text="视频下载",
            fg_color="transparent", 
            text_color=Theme.COLOR_TEXT_SECONDARY, 
            hover_color=Theme.COLOR_SECONDARY,
            anchor="w", 
            command=self.home_button_event,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY)
        )
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.convert_button = ctk.CTkButton(
            self.navigation_frame, 
            corner_radius=Theme.CORNER_RADIUS, 
            height=40, 
            border_spacing=10, 
            text="格式转换",
            fg_color="transparent", 
            text_color=Theme.COLOR_TEXT_SECONDARY, 
            hover_color=Theme.COLOR_SECONDARY,
            anchor="w", 
            command=self.convert_button_event,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY)
        )
        self.convert_button.grid(row=2, column=0, sticky="ew")

        self.transcribe_button = ctk.CTkButton(
            self.navigation_frame, 
            corner_radius=Theme.CORNER_RADIUS, 
            height=40, 
            border_spacing=10, 
            text="提取文字",
            fg_color="transparent", 
            text_color=Theme.COLOR_TEXT_SECONDARY, 
            hover_color=Theme.COLOR_SECONDARY,
            anchor="w", 
            command=self.transcribe_button_event,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY)
        )
        self.transcribe_button.grid(row=3, column=0, sticky="ew")
        
        # Appearance Mode
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.navigation_frame, 
            values=["System", "Light", "Dark"],
            command=self.change_appearance_mode_event,
            fg_color=Theme.COLOR_SECONDARY,
            button_color=Theme.COLOR_PRIMARY,
            button_hover_color=Theme.COLOR_PRIMARY_HOVER,
            text_color=Theme.COLOR_TEXT_PRIMARY,
            dropdown_fg_color=Theme.COLOR_SURFACE,
            dropdown_text_color=Theme.COLOR_TEXT_PRIMARY,
            corner_radius=Theme.CORNER_RADIUS
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # 2. Frames
        self.download_view = DownloadView(self, corner_radius=Theme.CORNER_RADIUS, fg_color="transparent")
        self.convert_view = ConvertView(self, corner_radius=Theme.CORNER_RADIUS, fg_color="transparent")
        self.transcribe_view = TranscribeView(self, corner_radius=Theme.CORNER_RADIUS, fg_color="transparent")

        # Select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # Update button colors
        self.home_button.configure(fg_color=Theme.COLOR_SECONDARY if name == "home" else "transparent")
        self.convert_button.configure(fg_color=Theme.COLOR_SECONDARY if name == "convert" else "transparent")
        self.transcribe_button.configure(fg_color=Theme.COLOR_SECONDARY if name == "transcribe" else "transparent")

        # Show selected frame
        if name == "home":
            self.download_view.grid(row=0, column=1, sticky="nsew")
        else:
            self.download_view.grid_forget()
            
        if name == "convert":
            self.convert_view.grid(row=0, column=1, sticky="nsew")
        else:
            self.convert_view.grid_forget()
            
        if name == "transcribe":
            self.transcribe_view.grid(row=0, column=1, sticky="nsew")
        else:
            self.transcribe_view.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def convert_button_event(self):
        self.select_frame_by_name("convert")

    def transcribe_button_event(self):
        self.select_frame_by_name("transcribe")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
