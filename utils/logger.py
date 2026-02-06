
import logging
import sys
from .config import PATHS

def setup_logger(name="video_downloader"):
    """配置并获取日志记录器"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # 避免重复添加handler
    if logger.handlers:
        return logger

    # 格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 文件处理器
    file_handler = logging.FileHandler(
        PATHS["logs"] / "app.log", 
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

# 全局logger实例
logger = setup_logger()
