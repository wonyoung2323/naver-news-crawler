import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from konlpy.tag import Kkma

kkma = Kkma()

wb = Workbook()
wb_1 = Workbook()
ws1 = wb.active
ws_1 = wb_1.active
ws1.title = "네이버 기사 크롤링"
ws_1.title = "형태소 분석"
ws1.append(["제목", "링크", "내용"])
ws_1.append(["분석"])

links = []
text_arr = []
hyungtaeso = []
search_keyword = input('enter keyword : ')

for page in range(1):
    url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query=' + \
        search_keyword + '&start=' + str(page * 10 + 1)
    # 페이지 접근 오류 해결
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'}
    r = requests.get(url)
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')

    if_naver = "news.naver"
    news_link = soup.select('.info_group > a')
    for i in range(len(news_link)):
        if if_naver in news_link[i]['href']:
            print(news_link[i]['href'])
            links.append(news_link[i]['href'])

    def get_content(URL):
        text = ''

        for item in news_sp.find_all('div', id='dic_area'):
            #text = text + str(item.find_all(text = True))
            text = item.get_text('\n', strip=True)
            return text

    for i in range(len(links)):
        news_r = requests.get(links[i], headers=headers)
        news_sp = BeautifulSoup(news_r.content, 'html.parser')
        news_titles = news_sp.select(
            '#title_area > span') or news_sp.select('.end_ct_area > h2')
        print(i + 1, news_titles[0].text)
        try:
            # 실행할 문장
            article = get_content(news_sp)
            print(article)
            r_article = article.replace(
                "// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}", "")
            text_arr.append(r_article)
        except Exception as e:
            # 오류를 무시하고 실행할 문장
            # entertain일 경우에 아무것도 저장 안함
            text_arr.append(" ")

        txt = text_arr[i]
        txt = txt.replace('. ', '.\n').split('.\n')
        for j in txt:
            hyungtaeso.append(kkma.pos(j))
        ws1.append([news_titles[0].text, links[i], text_arr[i]])

    for j in hyungtaeso:
        print(j)

# print(kkma.pos(txt[5]))
# print(kkma.pos(txt[5])[1][0])
# print(kkma.pos(txt[5])[1][1])
