#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import logging
from datetime import datetime, UTC
import time
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='indexnow-live.log',
    encoding='utf-8'
)

class SitemapIndexNowSubmitter:
    def __init__(self):
        self.api_endpoint = "https://api.indexnow.org/IndexNow"
        self.host = "livetv.izbds.com"
        self.key = "97231443a24b4c60b24728aa37560ddc"
        self.key_location = f"https://{self.host}/{self.key}.txt"
        self.sitemap_url = "https://livetv.izbds.com/sitemap.xml"
        self.max_retries = 3
        self.retry_delay = 5

    def get_urls_from_sitemap(self):
        """从 sitemap.xml 获取所有 URL"""
        try:
            response = requests.get(self.sitemap_url, timeout=30)
            if response.status_code != 200:
                logging.error(f"获取 sitemap 失败: {response.status_code}")
                return []

            # 解析 XML
            root = ET.fromstring(response.content)
            
            # 定义命名空间
            ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            
            # 提取所有 URL
            urls = []
            for url in root.findall('.//ns:url/ns:loc', ns):
                urls.append(url.text)
            
            logging.info(f"从 sitemap 中获取到 {len(urls)} 个 URL")
            return urls

        except Exception as e:
            logging.error(f"解析 sitemap 时发生错误: {str(e)}")
            return []

    def validate_url(self, url):
        """验证 URL 的有效性"""
        try:
            parsed = urlparse(url)
            return all([parsed.scheme, parsed.netloc])
        except:
            return False

    def submit_urls(self):
        # 获取 URL 列表
        url_list = self.get_urls_from_sitemap()
        if not url_list:
            logging.error("未能获取到有效的 URL 列表")
            return False

        # 验证所有 URL
        url_list = [url for url in url_list if self.validate_url(url)]
        if not url_list:
            logging.error("没有有效的 URL 可提交")
            return False

        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        
        payload = {
            "host": self.host,
            "key": self.key,
            "keyLocation": self.key_location,
            "urlList": url_list,
            "batchId": datetime.now(UTC).strftime("%Y%m%d%H%M%S"),
            "lastModified": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.api_endpoint,
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                logging.info(f"提交尝试 {attempt + 1}/{self.max_retries}")
                logging.info(f"状态码: {response.status_code}")
                logging.info(f"响应内容: {response.text}")
                
                if response.status_code == 200:
                    print(f"成功提交 {len(url_list)} 个 URL 到 IndexNow!")
                    logging.info(f"成功提交 {len(url_list)} 个 URL 到 IndexNow")
                    return True
                else:
                    print(f"提交失败，状态码: {response.status_code}")
                    logging.error(f"提交失败，状态码: {response.status_code}")
                    
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                        continue
                    return False
                    
            except Exception as e:
                print(f"发生错误: {str(e)}")
                logging.error(f"发生错误: {str(e)}")
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                return False

def main():
    submitter = SitemapIndexNowSubmitter()
    submitter.submit_urls()

if __name__ == "__main__":
    main() 