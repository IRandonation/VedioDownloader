
import yt_dlp
import os
from utils.logger import logger

class VideoDownloader:
    @staticmethod
    def fetch_video_info(url, cookie_file=None):
        """获取视频信息（异步任务中调用）"""
        try:
            logger.info(f"正在获取视频信息: {url}")
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': 'in_playlist', # 遇到列表时只提取基本信息，不深入解析每个视频，提高速度
            }
            if cookie_file and os.path.exists(cookie_file):
                ydl_opts['cookiefile'] = cookie_file

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return VideoDownloader._parse_info(info)

        except Exception as e:
            logger.error(f"获取信息异常: {e}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def _parse_info(info):
        """解析 yt-dlp 信息"""
        # 处理播放列表/合集
        if info.get('_type') == 'playlist' or ('entries' in info and not info.get('formats')):
            title = info.get("title", "未知列表")
            entry_count = len(list(info.get("entries", [])))
            return {
                "success": True,
                "title": f"[合集] {title} (共 {entry_count} 个视频)",
                "qualities": [
                    {
                        "id": "bestvideo+bestaudio/best",
                        "display": "最佳画质 (Best Quality) - 整单下载",
                        "size": 0,
                        "size_str": "Unknown",
                    },
                    {
                        "id": "bestaudio/best",
                        "display": "仅音频 (Audio Only) - 整单下载",
                        "size": 0,
                        "size_str": "Unknown",
                    }
                ],
                "thumbnail": None,
                "duration": None
            }

        title = info.get("title", "未知标题")
        formats = info.get("formats", [])
        qualities = []
        
        # 如果没有 formats (可能是某些非视频链接或特殊情况)，尝试直接使用 info
        if not formats:
             formats = [info]

        for f in formats:
            format_id = f.get('format_id')
            if not format_id:
                continue
                
            ext = f.get('ext', '')
            resolution = f.get('resolution')
            # 有些格式没有 resolution 字段，尝试用 height/width 拼接
            if not resolution and f.get('height'):
                resolution = f"{f.get('width', '?')}x{f.get('height')}"
            
            filesize = f.get('filesize') or f.get('filesize_approx') or 0
            note = f.get('format_note', '')
            vcodec = f.get('vcodec', 'none')
            acodec = f.get('acodec', 'none')

            # 简单的过滤逻辑：保留有视频流的格式，或者纯音频（如果用户需要的话，但这里主要是视频下载）
            # 或者我们全部列出，让用户选。
            # 为了体验更好，我们可以构造一个友好的 display 字符串
            
            # 格式化大小
            size_str = "Unknown"
            if filesize:
                size_mb = filesize / (1024 * 1024)
                size_str = f"{size_mb:.2f} MB"
            
            # 构建显示名称
            display_parts = []
            if resolution:
                display_parts.append(str(resolution))
            if note:
                display_parts.append(note)
            if ext:
                display_parts.append(ext)
            if vcodec != 'none':
                display_parts.append(f"v:{vcodec}")
            if acodec != 'none':
                display_parts.append(f"a:{acodec}")
            display_parts.append(size_str)
            
            display = " - ".join(display_parts)

            if vcodec != 'none' and acodec == 'none':
                # 如果是纯视频流，自动合并最佳音频
                actual_id = f"{format_id}+bestaudio"
            else:
                actual_id = format_id

            qualities.append({
                "id": actual_id,
                "container": ext,
                "quality": resolution or note or "Unknown",
                "size": filesize,
                "size_str": size_str,
                "display": display,
                "vcodec": vcodec,
                "acodec": acodec
            })
            
        # 排序：文件越大一般质量越好
        qualities.sort(key=lambda x: x["size"] or 0, reverse=True)
        
        return {
            "success": True,
            "title": title,
            "qualities": qualities,
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration")
        }

    @staticmethod
    def download_video(url, output_dir, quality_id=None, cookie_file=None, on_progress=None, cancel_event=None):
        """
        下载视频
        on_progress: 回调函数，接收 (percent, speed)
        cancel_event: threading.Event，用于取消下载
        """
        try:
            logger.info(f"开始下载: {url} -> {output_dir}")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            def progress_hook(d):
                if cancel_event and cancel_event.is_set():
                    raise Exception("下载已取消")

                if d['status'] == 'downloading':
                    if on_progress:
                        try:
                            p = d.get('_percent_str', '0%').replace('%', '')
                            percent = float(p)
                        except Exception:
                            percent = 0.0
                        
                        speed = d.get('_speed_str', '0B/s')
                        on_progress(percent, speed)
                elif d['status'] == 'finished':
                    if on_progress:
                        on_progress(100.0, "完成")

            ydl_opts = {
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
                'quiet': True,
                'no_warnings': True,
                # 确保合并后的格式为 mp4 (如果发生了合并)
                'merge_output_format': 'mp4',
            }

            if quality_id:
                ydl_opts['format'] = quality_id
            
            if cookie_file and os.path.exists(cookie_file):
                ydl_opts['cookiefile'] = cookie_file

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            return {"success": True, "message": "下载完成"}

        except Exception as e:
            logger.error(f"下载异常: {e}")
            return {"success": False, "message": str(e)}
