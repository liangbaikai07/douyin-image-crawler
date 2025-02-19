from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
import json
import logging
import webbrowser
from urllib.parse import urlparse
from pathlib import Path
from threading import Timer

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
CONFIG_FILE = 'config.json'

# 初始化下载目录
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def load_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"加载配置文件失败: {str(e)}")
    return {'driver_path': ''}

def save_config(data):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.error(f"保存配置文件失败: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_driver_path', methods=['POST'])
def save_driver_path():
    try:
        path = request.json.get('path', '')
        if not path:
            return jsonify(success=False, error="空路径")
        
        # 转换为绝对路径并验证
        abs_path = Path(path).resolve().as_posix()
        if not os.path.exists(abs_path):
            return jsonify(success=False, error="路径不存在")
        
        config = load_config()
        config['driver_path'] = abs_path
        save_config(config)
        return jsonify(success=True)
    except Exception as e:
        logger.error(f"保存路径失败: {str(e)}")
        return jsonify(success=False, error=str(e))

@app.route('/get_images', methods=['POST'])
def get_images():
    try:
        config = load_config()
        driver_path = config.get('driver_path', '')
        if not driver_path or not os.path.exists(driver_path):
            return jsonify(success=False, error="请先选择有效的ChromeDriver路径")
        
        url = request.json.get('url', '')
        if not url.startswith(('http://', 'https://')):
            return jsonify(success=False, error="无效的URL格式")

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        
        logger.debug(f"正在访问URL: {url}")
        driver.get(url)
        
        # 等待图片加载
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, '//img'))
        )
        
        images = []
        for img in driver.find_elements(By.XPATH, '//img'):
            src = img.get_attribute('src') or img.get_attribute('data-src')
            if src and src.startswith('http'):
                logger.debug(f"发现有效图片地址: {src}")
                images.append(src)
        
        driver.quit()
        return jsonify(success=True, images=images)
    
    except Exception as e:
        logger.error(f"获取图片失败: {str(e)}")
        return jsonify(success=False, error=str(e))


@app.route('/download', methods=['POST'])
def download_images():
    data = request.json
    results = []

    def download_file(url, index):
        try:
            # 生成顺序文件名
            seq = index + 1

            # 获取扩展名
            headers = {
                'Referer': 'https://www.douyin.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
            }

            with requests.get(url, headers=headers, stream=True, timeout=30) as response:
                response.raise_for_status()

                # 通过Content-Type获取文件类型
                content_type = response.headers.get('Content-Type', '')
                if 'image/jpeg' in content_type:
                    ext = 'jpg'
                elif 'image/png' in content_type:
                    ext = 'png'
                elif 'image/webp' in content_type:
                    ext = 'webp'
                else:  # 从URL解析扩展名
                    parsed = urlparse(url)
                    filename = os.path.basename(parsed.path)
                    ext = filename.split('.')[-1].lower() if '.' in filename else 'jpg'
                    ext = ext[:4]  # 防止过长扩展名

                # 生成最终文件名
                filename = f"{seq}.{ext}"
                save_path = os.path.join(DOWNLOAD_FOLDER, filename)

                # 写入文件
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

                # 验证文件有效性
                if os.path.getsize(save_path) < 1024:
                    os.remove(save_path)
                    raise ValueError("文件大小异常")

                return True, filename

        except Exception as e:
            logger.error(f"下载失败 {url}: {str(e)}")
            return False, str(e)

    # 遍历时携带索引信息
    for idx, url in enumerate(data.get('urls', [])):
        success, result = download_file(url, idx)
        results.append({
            'success': success,
            'url': url,
            'filename': result if success else None,
            'error': None if success else result
        })

    return jsonify(results=results)

def open_browser():
    webbrowser.open_new('http://localhost:5000')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(host='0.0.0.0', port=5000, debug=True)