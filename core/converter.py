
import subprocess
import os
import re
from utils.logger import logger

class MediaConverter:
    @staticmethod
    def get_duration(input_path):
        """获取媒体文件时长（秒）"""
        try:
            cmd = [
                "ffprobe", 
                "-v", "error", 
                "-show_entries", "format=duration", 
                "-of", "default=noprint_wrappers=1:nokey=1", 
                input_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return float(result.stdout.strip())
        except Exception as e:
            logger.error(f"获取时长失败: {e}")
            return 0

    @staticmethod
    def convert_to_audio(input_path, output_format="mp3", bitrate="192k", on_progress=None, cancel_event=None):
        """
        转换视频为音频
        """
        try:
            if not os.path.exists(input_path):
                return {"success": False, "message": "输入文件不存在"}

            input_dir = os.path.dirname(input_path)
            file_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(input_dir, f"{file_name}.{output_format}")

            logger.info(f"开始转换: {input_path} -> {output_path}")

            # 获取总时长用于计算进度
            total_duration = MediaConverter.get_duration(input_path)

            cmd = [
                "ffmpeg",
                "-i", input_path,
                "-vn", # 禁用视频流
                "-y",  # 覆盖输出
                "-b:a", bitrate,
                output_path
            ]

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding='utf-8'
            )

            # 解析 FFmpeg 进度
            # size=     512kB time=00:00:26.56 bitrate= 157.9kbits/s speed=53.1x
            time_pattern = re.compile(r'time=(\d{2}):(\d{2}):(\d{2}\.\d{2})')

            for line in process.stdout:
                if cancel_event and cancel_event.is_set():
                    process.terminate()
                    return {"success": False, "message": "已取消"}

                line = line.strip()
                match = time_pattern.search(line)
                if match and total_duration > 0:

                    h, m, s = map(float, match.groups())
                    current_time = h * 3600 + m * 60 + s
                    percent = min(100, (current_time / total_duration) * 100)
                    
                    if on_progress:
                        on_progress(percent)
                
            process.wait()

            if process.returncode == 0:
                return {"success": True, "message": "转换完成", "output_path": output_path}
            else:
                return {"success": False, "message": "转换失败"}

        except Exception as e:
            logger.error(f"转换异常: {e}")
            return {"success": False, "message": str(e)}
