import requests
from bs4 import BeautifulSoup
import bs4

#url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2018.html'
def getHTMLText(url): #获取服务器信息
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""



def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, "html.parser")
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            ulist.append([tds[0].string, tds[1].string, tds[3].string])




def printUnivList(ulist, num): #信息保存
    print("{:^10}\t{:^6}\t{:^10}".format('排名', '学校名称', '总分'))
    for i in range(num):
        u = ulist[i]
        print("{:^10}\t{:^6}\t{:^10}".format(u[0], u[1], u[2]))


def main():  #主函数
    uinfo = []
    url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2019.html'
    html = getHTMLText(url)
    fillUnivList(uinfo, html)
    printUnivList(uinfo, 40)#输出20个


main()
