import requests
from bs4 import BeautifulSoup

def Request(url):
    '''抓取网页'''
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'}#'accept-encoding':'utf-8'}

    try:
        r = requests.get(url,headers=headers,timeout=15)
        # print(r.encoding)
        # print(r.apparent_encoding)
        #r.encoding=r.apparent_encoding
        encoding = 'utf-8'
        return r.text
    except Exception as e:
        print(e)
        print('error')
        print(requests.get(url).status_code)
        #print(requests.raise_for_status())
        return False
        

def read_page(url):
    '''获取HTML'''
    if Request(url) != False:
        soup = BeautifulSoup(Request(url),'html.parser')
        page_content = soup.find_all('span',class_='short')
        return page_content
    
def write2txt(url,page):
    '''写入到文本文件中'''
    file = r"D:\GIT\comment_analysis\WandaVision.txt"
    with open(file,'a+',encoding = 'utf-8') as f:

        f.write(str(read_page(url)))

def main():
    '''在未登录状态下，豆瓣短评只能爬前十页'''
    page = 1
    for start in range(0,201,20):
        url = 'https://movie.douban.com/subject/30331433/comments?start='+str(start)+'&limit=20&status=P&sort=new_score'
        write2txt(url,page)
        page += 1
    print(page)
    
main()