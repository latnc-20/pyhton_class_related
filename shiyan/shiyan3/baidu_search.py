import requests
import json
from bs4 import BeautifulSoup


def get_query_result(keyword):
    try:
        url = "http://www.baidu.com/s?wd={}".format(keyword)
        kv = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
        r = requests.get(url, headers=kv, timeout=30)
        r.encoding = 'utf-8'
        return r.text
    except:
        return 'Get Error!'


def parser_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    """ print(soup.find(id="content_left"))
    
    for s in soup.find_all(name="div", attrs={"data-tools": True}):
        g = s.get_text()
        print(type(s))
        print(s)
    # print(soup.prettify())

    article_title = []
    for s in soup.select('#content_left .t a'):  # '#'后表示id=content_left的元素，'.'表示class
        print(s)
        g_title = s.get_text().replace('\n', '').strip()
        article_title.append(g_title)

    return article_title
"""

    article_title = []
    for div in soup.find_all(name="div", attrs={"data-tools": True}):
        print(div)
        data = div.attrs['data-tools']  # 获取div的属性值
        d = json.loads(data)  # 将属性值转换为字典
        # my_list = [d['title'], d['url']]
        article_title.append(d['title'])

    return article_title


# keywords = input("请输入你想查询的关键词：")
keywords = '程序设计及应用'
txt = get_query_result(keywords)
article_titles = parser_links(txt)
for i in range(len(article_titles)):
    print("[{}]：{}".format(i+1, article_titles[i]))







