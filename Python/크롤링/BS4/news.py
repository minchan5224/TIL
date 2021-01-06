# -*- coding: utf-8 -*-

import requests
from urllib import parse
from bs4 import BeautifulSoup
"""
parse.quote() 이용해 url 인코딩.
parse.unquote() 이용해 디코딩.
"""

def google_newsclipping(limit=5):
    """
    Parameters
    ----------
    url : 클리핑 할 url
    limit : 몇개의 기사 가져올건지, 기본값은 5개.
    -------
    사용자가 입력한 키워드의 기사를 구글에서 수집하여 딕셔너리 형식으로 반환.
    """
    try:
        search_keyword = str(input("input keyword : ")) # 사용자가 입력한 키워드의 기사 클리핑한다.
    except KeyboardInterrupt:
        return "사용자가 종료를 요청 했습니다."
    base_url = "https://news.google.com"

    search_url = base_url + "/search?q="+parse.quote(search_keyword)+"&hl=ko&gl=KR&ceid=KR%3Ako"
    
    resp = requests.get(search_url)
    html_src = resp.text
    soup = BeautifulSoup(html_src, 'html.parser')
    news_items = soup.select('div[class="xrnccd"]')
    
    links = []; titles = []; contents = []; agencies = []; reporting_dates = []; reporting_times = [];
    
    for item in news_items[:limit]:

        link = item.find('a', attrs={'class':'VDXfz'}).get('href')
        links.append(base_url+link[1:]) # 링크 수집
        
        titles.append(item.find('a', attrs={'class':'DY5T1d'}).getText()) # 제목 수집
        try :
            contents.append(item.find('span', attrs={'class':'xBbh9'}).text) # 내용 수집
        except AttributeError:
            contents.append("내용 누락, 링크 확인.")
        
        agencies.append(item.find('a', attrs={'class':'wEwyrc AVN2gc uQIVzc Sksgp'}).text) # 출처 수집
        
        news_reporting = item.find('time', attrs={'class':'WW6dff uQIVzc Sksgp'}) # 시간 수집
        try :
            news_reporting_datetime = news_reporting.get('datetime').split('T')
            reporting_dates.append(news_reporting_datetime[0])
            reporting_times.append(news_reporting_datetime[1][:-1])
            
        except AttributeError:
            reporting_dates("작성 일 누락")
            reporting_times("작성 시간 누락")
            
    result = {'link':links, 'title':titles, 'content':contents, 'agency':agencies, 'dete':reporting_dates, 'time':reporting_times}

    return result

news = google_newsclipping()
print(news)

