#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import logging
from datetime import datetime

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

    def submit_urls(self):
        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        
        payload = {
            "host": self.host,
            "key": self.key,
            "keyLocation": self.key_location,
            "urlList": self.url_list
        }

        try:
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=payload
            )
            
            logging.info(f"状态码: {response.status_code}")
            logging.info(f"响应内容: {response.text}")
            
            if response.status_code == 200:
                print("成功提交 URL 到 IndexNow!")
                logging.info("成功提交 URL 到 IndexNow")
                return True
            else:
                print(f"提交失败，状态码: {response.status_code}")
                logging.error(f"提交失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"发生错误: {str(e)}")
            logging.error(f"发生错误: {str(e)}")
            return False

def main():
    submitter = IndexNowSubmitter()
    submitter.submit_urls()

if __name__ == "__main__":
    main() 