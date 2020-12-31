import requests
from bs4 import BeautifulSoup
import re
import csv


def save2excel(new_list):
    with open(r'data1.xls', 'a', newline='', encoding='utf-8-sig') as f:
        csv_writer = csv.writer(f)  # 读取
        csv_writer.writerow(new_list)  # 写入


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}


def request_get(url, headers=headers):
    '''
    最后返回页面的网址
    :param url: 网页url
    :param headers: headers
    :return:html
    '''
    r = requests.get(url, headers=headers)
    html = BeautifulSoup(r.text, 'lxml')
    return html


def csdn_data(url):
    '''
    获取csdn的数据
    :param url:
    :return: name, amount
    '''
    html = request_get(url)
    pattern_1 = '<h1 class="title-article" id="articleContentId">(.+)</h1>'
    pattern_2 = '<span class="read-count">(.+)</span>'
    name = re.findall(pattern_1, str(html.body))
    amount = re.findall(pattern_2, str(html.body))
    # print(name, amount)
    return name, amount


def aibaidu_data(url):
    '''
    获取百度社区的数据
    :param url:
    :return: name amount
    '''
    try:
        html = request_get(url)
        body = html.body
        name = body.find('div', class_='f-brief-topic-cont').span.text
        amount = body.find('div', class_='f-release-message').find_all('span')[-2].text
    except:
        name = amount = []
    return name, amount


def oschina_data(url):
    '''
    获取开源中国的数据
    :param url:
    :return: name amount
    '''
    html = request_get(url)
    pattern_1 = 'val data-name="weixinShareTitle" data-value="(.+)"></val> <val data-name="'
    pattern_2 = '<div class="item lm">阅读数(.+)</div>'
    name = re.findall(pattern_1, str(html.body))
    amount = re.findall(pattern_2, str(html.body))
    return name, amount


def cnblogs_data(url):
    '''
    获取博客园的数据
    :param url:
    :return: name, amount
    '''
    try:
        r = requests.get(url, headers=headers)
        html = BeautifulSoup(r.text, 'lxml')
        name = html.body.find('a', id='cb_post_title_url').span.text
        amount = html.body.find('span', id='post_view_count').text
    except:
        name = amount = []
    return name, amount


def list_append(url, p1, p2, tmp=[]):
    '''
    处理得到的数据写入csv
    :param url: 链接
    :param p1: 文章名字列表
    :param p2: 浏览次数列表
    :param tmp: 空列表
    :return: None
    '''
    if p1 != []:  # 有数据
        tmp.append(url[:-1])
        if len(p1[0]) == 1:
            tmp.append(p1[:])
        else:
            tmp.append(p1[0])
        tmp.append(p2[0])
        save2excel(tmp)
        print(tmp)
        tmp.clear()  # 清空列表

    else:  # 无数据
        print(f'{url[:-1]}  文章链接失效')
        tmp.append(url[:-1])
        tmp.append("文章链接失效")
        tmp.append(0)
        save2excel(tmp)
        tmp.clear()
        print(tmp)



if __name__ == '__main__':
    title = ['url', 'title', 'num']
    save2excel(title)  # 写入文件头
    with open('链接.txt', 'r', encoding='utf-8')as f:  # 读取数据需要更据实际情况修改
        '''
        此处的格式在链接最后添加了一个\n所以后面的链接多加了一个[:-1]
        '''
        urles = f.read()
        # print(urles)
        one_url = ''
        url_list = []
        for urle in urles:
            one_url += urle
            if urle == '\n':
                url_list.append(one_url)
                one_url = ''


    for url in url_list:  # 判断链接属于哪个网站
        if url[:22] == 'https://blog.csdn.net/':
            # print(url[:-1])
            p1, p2 = csdn_data(str(url[:-1]))
            list_append(url[:-1], p1, p2)
        if url[:22] == 'https://my.oschina.net':
            p1, p2 = oschina_data(str(url[:-1]))
            list_append(url[:-1], p1, p2)
        if url[:23] == 'https://www.cnblogs.com':
            p1, p2 = cnblogs_data(str(url[:-1]))
            list_append(url[:-1], p1, p2)
        if url[:20] == 'https://ai.baidu.com':
            p1, p2 = aibaidu_data(str(url[:-1]))
            list_append(url[:-1], p1, p2)
        else:
            pass
