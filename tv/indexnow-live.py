#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import logging
from datetime import datetime, UTC
import time
from urllib.parse import urlparse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='indexnow.log'
)

class IndexNowSubmitter:
    def __init__(self):
        self.api_endpoint = "https://api.indexnow.org/IndexNow"
        self.host = "izbds.com"
        self.key = "10494a0749004fd3b5260106760f3d2b"
        self.key_location = f"https://{self.host}/{self.key}.txt"
        
        self.url_list = [
            "https://live.izbds.com",
            "https://live.izbds.com/tv/iptv6.txt",
            "https://live.izbds.com/tv/iptv6.m3u",
            "https://live.izbds.com/tv/iptv4.txt",
            "https://live.izbds.com/tv/iptv4.m3u"
        ]
        self.max_retries = 3
        self.retry_delay = 5  # 重试间隔秒数

    def validate_url(self, url):
        """验证 URL 的有效性"""
        try:
            parsed = urlparse(url)
            return all([parsed.scheme, parsed.netloc])
        except:
            return False

    def submit_urls(self):
        # 验证所有 URL
        if not all(self.validate_url(url) for url in self.url_list):
            logging.error("URL 列表包含无效的 URL")
            return False

        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        
        payload = {
            "host": self.host,
            "key": self.key,
            "keyLocation": self.key_location,
            "urlList": self.url_list,
            "lastModified": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.api_endpoint,
                    headers=headers,
                    json=payload,
                    timeout=30  # 添加超时设置
                )
                
                logging.info(f"提交尝试 {attempt + 1}/{self.max_retries}")
                logging.info(f"状态码: {response.status_code}")
                logging.info(f"响应内容: {response.text}")
                
                if response.status_code == 200:
                    print("成功提交 URL 到 IndexNow!")
                    logging.info("成功提交 URL 到 IndexNow")
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
    submitter = IndexNowSubmitter()
    submitter.submit_urls()

if __name__ == "__main__":
    main() 