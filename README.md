# 🎬 视频下载器

一个基于Python的现代化视频下载工具，支持多平台视频下载和音视频格式转换。

## ✨ 功能特性

### 🚀 核心功能
- **多平台支持**: 支持YouTube、Bilibili、抖音、微博等主流视频网站
- **智能下载**: 基于yt-dlp引擎，自动识别视频源
- **质量选择**: 支持多种视频质量选项（最佳、720p、480p、360p等）
- **Cookie登录**: 支持导入Cookie文件下载需要登录的内容
- **路径自定义**: 可自由选择下载保存路径

### 🎵 格式转换
- **多格式支持**: 支持MP4、MP3、WAV、FLAC、AAC等格式
- **音频转换**: 基于FFmpeg的高质量音频转换
- **比特率选择**: 支持64k-320k多种音频比特率
- **批量处理**: 支持单文件转换和批量处理

### 🎨 界面设计
- **苹果风格**: 简约现代的界面设计
- **中文优化**: 完美支持中文字符渲染
- **响应式布局**: 自适应窗口大小调整
- **实时日志**: 详细的操作日志和进度显示

## 📋 系统要求

### 必需依赖
- **Python**: 3.9或更高版本
- **you-get**: 视频下载引擎
- **ffmpeg**: 音视频处理工具

### Python包依赖
- `you-get`: 视频下载
- `ffmpeg-python`: FFmpeg Python接口
- `pillow`: 图像处理
- `requests`: HTTP请求处理

## 🛠️ 安装指南

### 1. 克隆项目
```bash
git clone <repository-url>
cd vedioDownload
```

### 2. 安装依赖
项目使用uv作为包管理器：

```bash
# 安装uv（如果尚未安装）
pip install uv

# 同步项目依赖
uv sync
```

### 3. 安装外部工具

#### Windows
```bash
# 安装yt-dlp
pip install yt-dlp

# 安装ffmpeg
# 下载ffmpeg并添加到系统PATH
# 或使用chocolatey: choco install ffmpeg
```

#### macOS
```bash
# 使用Homebrew安装
brew install you-get ffmpeg
```

#### Linux
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install you-get ffmpeg

# CentOS/RHEL
sudo yum install you-get ffmpeg
```

## 🚀 使用方法

### 启动应用
```bash
# 使用uv运行
uv run python main.py

# 或使用启动脚本
uv run python run.py
```

### 基本操作

#### 1. 视频下载
1. 在"视频链接"框中输入视频URL
2. 选择视频质量（可选）
3. 选择下载路径
4. 点击"🚀 开始下载"

#### 2. Cookie登录下载
1. 导出浏览器Cookie为txt文件
2. 点击"浏览"选择Cookie文件
3. 输入需要登录的视频链接
4. 开始下载

#### 3. 格式转换
1. 点击"🔄 转换文件"
2. 选择要转换的文件
3. 选择输出格式和音频比特率
4. 等待转换完成

### Cookie文件获取

#### Chrome浏览器
1. 安装"Get cookies.txt"扩展
2. 访问目标网站并登录
3. 点击扩展图标导出cookies.txt

#### Firefox浏览器
1. 安装"cookies.txt"扩展
2. 访问目标网站并登录
3. 导出cookies.txt文件

## 📁 项目结构

```
vedioDownload/
├── main.py              # 主应用程序
├── config.py            # 配置文件
├── run.py               # 启动脚本
├── pyproject.toml       # 项目配置
├── README.md            # 项目说明
├── assets/              # 资源文件
├── logs/                # 日志文件
├── downloads/           # 默认下载目录
└── .python-version      # Python版本
```

## ⚙️ 配置说明

### 界面配置
可在`config.py`中自定义：
- 窗口大小和最小尺寸
- 颜色主题和字体
- 间距和布局参数

### 下载配置
- 默认下载质量
- 支持的视频格式
- 音频比特率选项
- 默认保存路径

## 🔧 故障排除

### 常见问题

#### 1. you-get未找到
```bash
# 确保you-get已安装并在PATH中
pip install you-get
you-get --version
```

#### 2. ffmpeg未找到
```bash
# 检查ffmpeg安装
ffmpeg -version

# Windows用户需要将ffmpeg添加到系统PATH
```

#### 3. 下载失败
- 检查网络连接
- 验证视频链接有效性
- 尝试使用Cookie文件
- 查看日志获取详细错误信息

#### 4. 中文显示异常
- 确保系统已安装中文字体
- 检查系统区域设置
- 重启应用程序

### 日志文件
应用程序会在`logs/app.log`中记录详细日志，可用于问题诊断。

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发环境设置
```bash
# 克隆项目
git clone <repository-url>
cd vedioDownload

# 安装开发依赖
uv sync --dev

# 运行测试
uv run pytest

# 代码格式化
uv run black .
uv run flake8
```

## 📄 许可证

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件

## 🙏 致谢

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - 强大的视频下载工具
- [FFmpeg](https://ffmpeg.org/) - 多媒体处理框架
- [tkinter](https://docs.python.org/3/library/tkinter.html) - Python GUI框架

## 📞 支持

如有问题或建议，请：
1. 查看[常见问题](#故障排除)
2. 搜索现有[Issues](../../issues)
3. 创建新的Issue描述问题

---

**享受视频下载的乐趣！** 🎉