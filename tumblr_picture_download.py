# -*- coding: utf-8 -*-

import requests
import time
import os
from bs4 import BeautifulSoup

# 本地使用xx-net的代理
PROXIES = {
            'http': 'http://127.0.0.1:8087',
            'https': 'http://127.0.0.1:8087'
        }
HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
            'Cookie':'UID=1BF23a62a10944a424002ee1455808611; UIDR=1455808611'
        }
BASE_URL = ''
SAVE_IMG_PATH = ''

def save_img(img_url):
    time.sleep(1)
    img_name = img_url.split('/')[-1]
    img_content = requests.get(img_url, proxies=proxies).content
    img_path = SAVE_IMG_PATH+img_name
    if not os.path.exists(img_path):
        with open(img_path, 'wb+') as img:
            img.write(img_content)
            img.close()


def get_html_soup(url):
    html = requests.get(url, proxies=PROXIES, headers=HEADERS)
    soup = BeautifulSoup(html.text, "html.parser")
    return soup

def get_page_a_img(page_url):
    """
    获取页面中的img.src和a.href
    """
    soup = get_html_soup(page_url)
    img_urls = []
    a_hrefs = []
    for article in soup.find_all('article'):
        if article.find('img'):
            img_url = article.find('img')['src']
            img_urls.append(img_url)
        if article.find('a'):
            a_href = article.find('a')['href']
            a_hrefs.append(a_href)

    return img_urls, a_hrefs

def get_post_page_img_url(post_url):
    """
    获取图片组的图片地址
    """
    img_urls = []
    if 'tumblr' in post_url and post_url.endswith('#notes'):
        post_link = post_url.split('#')[0]
        post_id = post_link.split('/')[-1]
        post_soup = get_html_soup(post_link)
        iframe_html = post_soup.find(id='photoset_iframe_'+post_id)
        if iframe_html:
            img_url = iframe_html['src']
            img_soup = get_html_soup(img_url)
            for a_tag in img_soup.find_all('a'):
                if a_tag['href']:
                    img_urls.append(a_tag['href'])
    return img_urls

if __name__ == '__main__':
    page_img_count = 0
    post_img_count = 0
    for i in range(1, 100):
        page_url = BASE_URL % str(i)
        img_urls, a_hrefs = get_page_a_img(page_url)
        if (not img_urls) and (not a_hrefs):
            break
        for img_url in img_urls:
            save_img(img_url)
            page_img_count += 1

        for post_url in a_hrefs:
            time.sleep(1)
            post_img_urls = get_post_page_img_url(post_url)
            for img_url in post_img_urls:
                save_img(img_url)
                post_img_count += 1
        time.sleep(1)

