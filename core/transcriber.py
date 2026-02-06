
import os
import whisper
import torch
import warnings
from utils.logger import logger
from datetime import timedelta

# 忽略 FP16 警告 (如果 CPU 运行)
warnings.filterwarnings("ignore")

class VideoTranscriber:
    _model_cache = {}

    @staticmethod
    def _get_model(model_name, device=None):
        """获取或加载模型"""
        # 确定设备
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        
        cache_key = (model_name, device)
        
        if cache_key not in VideoTranscriber._model_cache:
            logger.info(f"正在加载 Whisper 模型: {model_name} (Device: {device})...")
            try:
                VideoTranscriber._model_cache[cache_key] = whisper.load_model(model_name, device=device)
            except Exception as e:
                # 如果加载失败（例如显存不足或CUDA错误），尝试回退到CPU
                if device == "cuda":
                    logger.warning(f"GPU加载失败，尝试使用CPU: {e}")
                    device = "cpu"
                    cache_key = (model_name, device)
                    if cache_key not in VideoTranscriber._model_cache:
                        VideoTranscriber._model_cache[cache_key] = whisper.load_model(model_name, device=device)
                else:
                    raise e
                    
        return VideoTranscriber._model_cache[cache_key]

    @staticmethod
    def transcribe(input_path, model_name="base", output_format="txt", use_gpu=True, on_progress=None):
        """
        提取视频/音频文字
        """
        try:
            if not os.path.exists(input_path):
                return {"success": False, "message": "输入文件不存在"}

            # 准备输出路径
            input_dir = os.path.dirname(input_path)
            file_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(input_dir, f"{file_name}.{output_format}")

            # 确定设备
            device = "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
            logger.info(f"计划使用设备: {device}")

            # 加载模型
            if on_progress:
                on_progress("正在加载模型...", 0)
            
            model = VideoTranscriber._get_model(model_name, device)

            # 获取音频时长用于进度计算
            try:
                audio = whisper.load_audio(input_path)
                duration = len(audio) / whisper.audio.SAMPLE_RATE
                print(f"DURATION: {duration}", flush=True)
            except Exception as e:
                logger.warning(f"无法获取音频时长: {e}")

            if on_progress:
                on_progress("正在转录中 (这可能需要一些时间)...", 10)

            # 开始转录
            logger.info(f"开始转录: {input_path}")
            
            # 使用 verbose=True 输出进度到 stdout，以便外部进程捕获
            result = model.transcribe(input_path, verbose=True)
            
            # 保存结果
            text = result["text"]
            segments = result["segments"]

            with open(output_path, "w", encoding="utf-8") as f:
                if output_format == "txt":
                    f.write(text)
                elif output_format == "srt":
                    for i, segment in enumerate(segments, start=1):
                        start = str(timedelta(seconds=int(segment["start"]))) + ",000"
                        end = str(timedelta(seconds=int(segment["end"]))) + ",000"
                        f.write(f"{i}\n{start} --> {end}\n{segment['text'].strip()}\n\n")
                elif output_format == "vtt":
                    f.write("WEBVTT\n\n")
                    for i, segment in enumerate(segments, start=1):
                        start = str(timedelta(seconds=int(segment["start"]))) + ".000"
                        end = str(timedelta(seconds=int(segment["end"]))) + ".000"
                        f.write(f"{start} --> {end}\n{segment['text'].strip()}\n\n")
            
            if on_progress:
                on_progress("完成!", 100)

            result_data = {"success": True, "message": "转录完成", "output_path": output_path}
            print(f"RESULT: {result_data}", flush=True)
            return result_data

        except Exception as e:
            logger.error(f"转录异常: {e}")
            result_data = {"success": False, "message": str(e)}
            print(f"RESULT: {result_data}", flush=True)
            return result_data
