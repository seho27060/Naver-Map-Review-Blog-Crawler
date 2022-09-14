import re
import urllib

import requests
from bs4 import BeautifulSoup

def blogCrawler(url):
    response = requests.get(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    content = ""
    if response.status_code == 200:
        try:
            res = requests.get(url, headers=headers)
            res.raise_for_status()  # 문제시 프로그램 종료
            soup = BeautifulSoup(res.text, "html.parser")
            src_url = "https://blog.naver.com/" + soup.iframe["src"]
            response = requests.get(src_url,headers=headers)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            # print("phase 1")
            if soup.find(attrs={'class':"se-main-container"}):
                # print("phase2")
                content = soup.find(attrs={'class':"se-main-container"}).get_text()
                content = content.replace("\u200b", "")
                content = content.replace("\n", "")
                content = content.replace("Previous image", "")
                content = content.replace("Next image", "")
            else:
                if soup.find(attrs={'id': "postViewArea"}):
                    # print("phase3")
                    content = soup.find(attrs={'id': "postViewArea"}).get_text()
                    content = content.replace("\u200b", "")
                    content = content.replace("\n", "")
                    content = content.replace("Previous image", "")
                    content = content.replace("Next image", "")
                else:
                    print("본문없음")
        except:
            print("블로그 조회 실패")
    else:
        print(response.status_code)
    return content

# print(blogCrawler("https://blog.naver.com/babaks5/222677777105"))