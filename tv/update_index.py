import requests
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom
import pytz
import os

def update_sitemap():
    # 获取项目根目录的 sitemap.xml 路径
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sitemap_path = os.path.join(root_dir, 'sitemap.xml')
    
    # 读取现有的 sitemap.xml
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    
    # 获取中国时区的当前日期
    tz = pytz.timezone('Asia/Shanghai')
    current_date = datetime.now(tz).strftime('%Y-%m-%d')
    
    # 更新所有 URL 的 lastmod
    for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        lastmod = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
        if lastmod is not None:
            lastmod.text = current_date
    
    # 转换为格式化的 XML 字符串
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent='    ')
    # 移除空行
    xmlstr = '\n'.join([s for s in xmlstr.splitlines() if s.strip()])
    
    # 保存更新后的 sitemap
    with open(sitemap_path, 'w', encoding='UTF-8') as f:
        f.write(xmlstr)
    print(f"Sitemap updated with date: {current_date}")

def notify_index_now():
    urls = [
        "https://live.zbds.top",
        "https://live.zbds.top/tv/iptv6.txt",
        "https://live.zbds.top/tv/iptv6.m3u",
        "https://live.zbds.top/tv/iptv4.txt",
        "https://live.zbds.top/tv/iptv4.m3u",
        "https://live.zbds.top/tools/"
    ]
    
    for site_url in urls:
        url = "https://www.bing.com/indexnow"
        params = {
            "url": site_url,
            "key": "4c761c7c12a64659b9529b778f6a3b75"
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print(f"Successfully notified IndexNow for {site_url}")
        else:
            print(f"Failed to notify IndexNow for {site_url}: {response.status_code}")

if __name__ == "__main__":
    update_sitemap()
    notify_index_now() 