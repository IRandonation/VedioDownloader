# Video Downloader

基于 Python 开发的现代化视频下载、转换与处理工具。集成了视频下载、格式转换和语音转文字功能，采用 CustomTkinter 构建现代化暗色主题 UI。

## ✨ 主要功能

- **视频下载**：集成 `yt-dlp`，支持主流视频网站视频下载。
- **格式转换**：基于 `ffmpeg`，支持多种音视频格式互转。
- **语音转文字**：集成 OpenAI `Whisper` 模型，支持本地语音识别与字幕提取。
- **现代化 UI**：使用 `CustomTkinter` 构建，支持高分屏适配与暗色模式。

## 🛠️ 技术栈

- **GUI**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- **下载引擎**: [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **多媒体处理**: [FFmpeg](https://ffmpeg.org/) (via `ffmpeg-python`)
- **语音识别**: [OpenAI Whisper](https://github.com/openai/whisper)
- **依赖管理**: [uv](https://github.com/astral-sh/uv)

## 📦 安装说明

### 前置要求

1. **Python 3.9+**
2. **FFmpeg**: 必须安装并添加到系统环境变量 PATH 中。
3. **CUDA (可选)**: 如果需要 GPU 加速 Whisper 语音识别，建议安装 NVIDIA CUDA Toolkit。

### 步骤

1. 克隆仓库：
   ```bash
   git clone https://github.com/IRandonation/VedioDownloader.git
   cd VedioDownloader
   ```

2. 安装依赖（推荐使用 uv）：
   ```bash
   # 安装 uv (如果尚未安装)
   pip install uv

   # 同步依赖环境
   uv sync
   ```
   或者使用 pip：
   ```bash
   pip install .
   ```

## 🚀 运行

使用 uv 运行（推荐）：
```bash
uv run main.py
```

或者在激活的虚拟环境中直接运行：
```bash
python main.py
```

## 📂 项目结构

```
.
├── core/               # 核心逻辑模块
│   ├── downloader.py   # 视频下载逻辑
│   ├── converter.py    # 格式转换逻辑
│   └── transcriber.py  # 语音识别逻辑
├── ui/                 # 用户界面
│   ├── views/          # 各功能页面视图
│   └── app.py          # 主应用窗口配置
├── utils/              # 工具类 (配置、日志等)
├── assets/             # 资源文件
├── main.py             # 程序入口
├── pyproject.toml      # 项目配置与依赖
└── uv.lock             # 依赖锁定文件
```

## 📝 注意事项

- 首次运行语音识别功能时，Whisper 会自动下载模型文件，可能需要一定时间。
- 确保网络环境可以连接到 Hugging Face 或相关模型仓库。
