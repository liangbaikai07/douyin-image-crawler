# douyin-image-crawler
# 本人零基础，本项目完全使用Deepseek-r1开发，如有缺陷请见谅
# Douyin 图文爬虫

这是一个简单高效的抖音图文爬虫，用于从抖音（TikTok中国版）抓取图片、视频等媒体内容。该项目旨在帮助你根据提供的 URL 下载并存储抖音的媒体内容。

## 特性

- **提取图片和视频**：下载抖音用户个人资料和帖子中的图片缩略图和视频内容。
- **易于使用**：通过 Flask 提供简洁的后端服务。
- **轻量级**：最小依赖，快速爬取和下载内容。

## 环境要求

在运行该项目之前，确保已安装以下环境：

- Python 3.x
- `pip` 用于安装 Python 依赖
- chromedriver下载地址：
版本在114及以下：http://chromedriver.storage.googleapis.com/index.html
版本在127：https://googlechromelabs.github.io/chrome-for-testing/#stable
- 其他版本下载方法：
如版本127.0.6533 32位下载地址是：
https://storage.googleapis.com/chrome-for-testing-public/127.0.6533.100/win32/chromedriver-win32.zip

你还需要安装以下 Python 包：

```bash
pip install -r requirements.txt
本项目使用 Selenium 进行网页爬取，Flask 提供网页界面。

安装步骤
克隆该项目：

bash
git clone https://github.com/liangbaikai07/douyin-web-scraper.git
cd douyin-web-scraper
安装所需依赖：

bash
pip install -r requirements.txt
下载与操作系统匹配的 ChromeDriver，并确保它在系统的 PATH 环境变量中。

启动 Flask 应用：

bash
python app.py
通过浏览器访问 http://127.0.0.1:5000 来使用该应用。

使用方法
打开浏览器，访问 http://127.0.0.1:5000。
将抖音（Douyin/TikTok中国版）视频 URL 粘贴到输入框中。
点击“下载”按钮来获取图片和视频。
提取的图片和视频将显示在页面上，便于下载。
工作原理
该项目使用 Selenium 自动化浏览器，从提供的抖音 URL 中提取媒体内容（图片、视频）。然后通过网页界面将提取的媒体显示出来，供用户下载。

爬取流程：
用户提供一个抖音视频 URL。
应用使用 Selenium 加载该页面并抓取媒体（图片、视频）内容。
提取的媒体 URL 返回到前端页面供用户查看和下载。

贡献
欢迎 fork 本项目并提交 pull request。如果遇到 bug 或有任何改进建议，请开 issue。

许可
该项目使用 MIT 许可证 - 详情见 LICENSE 文件。

致谢
Selenium - 用于浏览器自动化。
Flask - 用于创建网页界面。
Douyin（抖音） - 本爬虫的目标平台。
