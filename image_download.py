import os
import time
import requests
from lxml import etree
from urllib import request
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}


def parse_page(url):
    response = requests.get(url=url, headers=headers)
    content = response.content.decode()
    return content

def get_image_info(content):
    mytree = etree.HTML(content)
    img_link_list = mytree.xpath('//ignore_js_op/img/@zoomfile')
    img_title_list = mytree.xpath('//ignore_js_op/img/@title')
    folder_name = mytree.xpath('//h1/text()')[0]
    return folder_name, img_link_list, img_title_list

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        return folder_name
    

def image_download(folder_name, img_link, img_title):
    try:
        filename = os.path.join(folder_name, img_title)
        img_response = requests.get(url=img_link, headers=headers, timeout=5)
        with open(filename, 'wb') as f:
            f.write(img_response.content)
        print(f"{os.path.basename(filename)} 下载完成")
    except Exception as e:
        print(f"{img_link}下载失败, {e}")

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size

def main():
    url = input("请输入链接: ")
    content = parse_page(url)
    folder_name, img_link_list, img_title_list = get_image_info(content)
    if create_folder(folder_name):
        with ThreadPoolExecutor() as executor:
            executor.map(image_download, [folder_name] * len(img_link_list), img_link_list, img_title_list)
        file_count = len([f for f in os.listdir(folder_name)])
        folder_size = get_folder_size(folder_name)
        print(f"已下载{file_count}张图片, 文件大小: {folder_size / (1024*1024):.2f}MB, {folder_name}下载完成!")
    else:
        print("文件已存在")



while True:
    print("1. 下载图片")
    print("2. 退出程序")
    choice = input("请输入你的选项: ")
    if choice == "1":
        main()
    elif choice == "2":
        print("感谢使用!")
        time.sleep(1.5)
        break
    else:
        print("输入错误, 请重新输入")
    