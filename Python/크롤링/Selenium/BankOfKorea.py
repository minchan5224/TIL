# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 17:39:01 2021

@author: Administrator

14~15 예제 작성.

"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time

def download_bok_statistics():
    """
    100대 통계지표 엑셀 다운로드
    """
    driver = webdriver.Chrome("../chromedriver_win32/chromedriver")
    driver.implicitly_wait(3)
    driver.get("https://ecos.bok.or.kr/jsp/vis/keystat/#/key/")
    
    excel_download = driver.find_element_by_css_selector('img[alt="download"]')
    driver.implicitly_wait(3)
    
    excel_download.click()
    time.sleep(5)
    
    driver.close()
    print("파일 다운로드 중")

    return None

def download_bok_statistics_by_keyword():
    """
    통계지표 키워드 입력하여 csv파일로 저장
    """
    item_found = 0
    while not item_found:
        
        keyword = ""
        
        while len(keyword) == 0:
            keyword = str(input("input keyword : "))
            
        driver = webdriver.Chrome("../chromedriver_win32/chromedriver")
        driver.implicitly_wait(3)
        driver.get("https://ecos.bok.or.kr/jsp/vis/keystat/#/key/")
        time.sleep(5)
        
        items1 = driver.find_elements_by_css_selector('a[class="ng-binding"]')
        items2 = driver.find_elements_by_css_selector('a[class="a-c1-list ng-binding"]')
        items3 = driver.find_elements_by_css_selector('a[class="a-c4-list ng-binding"]')
        driver.implicitly_wait(3)
        
        items = items1[1:]+items2+items3
        
        for idx, item in enumerate(items):
            if keyword in item.text:
                print("검색어 '%s'에 매칭되는 '%s' 통계지표를 검색" %(keyword, item.text))
                item.click()
                item_found = 1
                time.sleep(5)
                break
            elif idx == (len(items) - 1):
                print("검색어 '%s'에 대한 통계지표가 존재하지 않습니다." %keyword)
                driver.close()
                continue
            else:
                pass
        
    html_src = driver.page_source
    soup = BeautifulSoup(html_src, 'html.parser')
    driver.close()
    
    table_items = soup.find_all('td', {'class':'ng-binding'})
        
    date=[]; value=[]; change=[];
        
    for i, t in enumerate(table_items):
        if i % 3 == 0:
            date.append(t.text)
        elif i % 3 == 1:
            value.append(t.text)
        elif i % 3 == 2:
            change.append(t.text)
    
    result_file = open('../data/bok_statistics_%s.csv' % keyword, 'w')
    
    for i in range(len(date)):
        result_file.write("%s, %s, %s" % (date[i], value[i], change[i]))
        result_file.write('\n')
        
    result_file.close()
    print("키워드 '%s'에 대한 통계지표를 저장" % keyword)
    
    return date, value, change

result = download_bok_statistics_by_keyword()
print(result)
# download_bok_statistics()