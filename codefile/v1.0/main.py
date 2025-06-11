# -*- coding: utf-8 -*-

import sys
import requests
import re

def get_bvid(input_str):
    if input_str.startswith('BV') and len(input_str) == 12:
        return input_str
    match = re.search(r'(BV[0-9a-zA-Z]{10})', input_str)
    return match.group(1) if match else None

def get_video_info(bvid):
    api_url = f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'
    response = requests.get(api_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0'})
    if response.status_code != 200:
        return None
    data = response.json()
    if data['code'] != 0:
        return None
    return data['data']

def get_video_url(bvid, cid, quality=80):
    api_url = f'https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&qn={quality}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
        'Referer': 'https://www.bilibili.com/'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        return None
    data = response.json()
    if data['code'] != 0:
        return None
    return data['data']['durl'][0]['url']

def main():
    if len(sys.argv) != 5 or sys.argv[1].lower() != 'bv':
        print("使用方法: python ZZSB.py bv <bvid或视频URL> <fpmi> <fpma>")
        print("示例1: python ZZSB.py bv BV1GJ411x7h7 1 1")
        print("示例2: python ZZSB.py bv https://www.bilibili.com/video/BV1GJ411x7h7 1 1")
        return
    
    input_str = sys.argv[2]
    bvid = get_bvid(input_str)
    if not bvid:
        print("错误: 无效的BV号或视频URL")
        return
    
    try:
        fpmi = int(sys.argv[3])
        fpma = int(sys.argv[4])
    except ValueError:
        print("错误: fpmi和fpma必须是整数")
        return
    
    video_info = get_video_info(bvid)
    if not video_info:
        print("获取视频信息失败")
        return
    
    video_title = video_info['title']
    total_pages = len(video_info['pages'])
    
    for i in range(fpmi, fpma + 1):
        if i > total_pages or i < 1:
            print(f"错误: 分P编号{i}超出范围(1-{total_pages})")
            continue
        
        page_info = video_info['pages'][i-1]
        cid = page_info['cid']
        part_title = page_info.get('part', '')
        
        if total_pages == 1:
            print(f"已经获取到《{video_title}》的地址")
        else:
            print(f"已经获取到《{video_title}》第{i}P《{part_title}》的地址")
        
        video_link = get_video_url(bvid, cid)
        if video_link:
            print(f"下载地址: {video_link}\n")
        else:
            print(f"无法获取视频P{i}的链接\n")

if __name__ == "__main__":
    main()
