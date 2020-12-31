import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
def getHTMLText(url):
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()  # 不是200报错
        # r.encoding = r.apparent_encoding
        return r.text
    except:
        return '产生错误'


url = 'https://www.cnblogs.com/parkin/p/13189067.html'
print(getHTMLText(url))