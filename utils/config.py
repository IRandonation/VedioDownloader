
import os
from pathlib import Path

# 应用程序信息
APP_NAME = "全能视频工具箱"
APP_VERSION = "2.0.0"

# 路径配置
PATHS = {
    "home": Path.home(),
    "downloads": Path.home() / "Downloads",
    "app_data": Path.home() / ".video_downloader_v2",
}

PATHS["logs"] = PATHS["app_data"] / "logs"
PATHS["temp"] = PATHS["app_data"] / "temp"

# 确保目录存在
for path in PATHS.values():
    path.mkdir(parents=True, exist_ok=True)

# 下载配置
DOWNLOAD_CONFIG = {
    "default_quality": "best",
    "supported_qualities": ["best", "worst"], # 实际会从yt-dlp动态获取
    "temp_dir": PATHS["temp"],
    "partial_suffix": ".part"
}

# 转换配置
CONVERT_CONFIG = {
    "supported_formats": ["mp3", "wav", "flac", "aac", "m4a"],
    "default_format": "mp3",
    "default_bitrate": "192k",
    "supported_bitrates": ["128k", "192k", "256k", "320k"]
}

# Whisper 配置
WHISPER_CONFIG = {
    "models": ["tiny", "base", "small", "medium", "large"],
    "default_model": "base",
    "output_formats": ["txt", "srt", "vtt"],
    "default_format": "txt"
}

# UI 配置
UI_CONFIG = {
    "window_width": 1000,
    "window_height": 800,
    "min_width": 800,
    "min_height": 600,
    "theme_color": "blue",
}
