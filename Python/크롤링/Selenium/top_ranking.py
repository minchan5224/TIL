from bs4 import BeautifulSoup# 패키지 설치
from urllib import parse, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from datetime import datetime
from pytz import timezone
from openpyxl import load_workbook
import pandas as pd
import time
import os
import openpyxl

url = 'https://best.aliexpress.com/'
top_url_txt = 'url/top_url.txt'
link_txt = 'url/category_urls/'
screenshot_name = './screenshot/test_'
img_down_route = './image/'
search_day = "%Y/%m/%d"


def excel_create(top_list, category_name):
    '''
    엑셀 파일로 저장하기.
    '''
    KST = datetime.now(timezone('Asia/Seoul'))
    s_time = KST.strftime(search_day)
    alarm = ''
    # pd_tmp = {'ITEM_CODE':[],'TITLE':[] ,'IMG_ROUTE':[], 'URL':[], 'TIME':[]}
    pd_tmp = {'ITEM_CODE':[],'TITLE':[] ,'IMG_ROUTE':[], 'URL':[]}
    for i in range(len(top_list)):
        item_links = []
        img_links = []
        item_names = []
        img_routes = []
        item_names, item_links, img_links = category_item_code(top_list[i], category_name[i])# 카테고리별로 txt파일로 나눠 저장
        if len(item_links) != 11:
            alarm += category_name[i]+' : lenge short\n'
        item_codes = item_code_extraction(item_links)
        img_routes = down_img(img_links, item_codes)
        
        pd_tmp['ITEM_CODE']+=item_codes
        pd_tmp['TITLE']+=item_names
        pd_tmp['IMG_ROUTE']+=img_routes
        pd_tmp['URL']+=item_links
        # pd_tmp['TIME']+=s_time
    # print(pd_tmp)
    create_ex = pd.DataFrame(pd_tmp)
    # create_ex = ex_tmp.to_frame()
    print(create_ex)
    print(alarm)
    create_ex.to_excel('./excel/output.xlsx')
    
def down_img(img_urls, img_codes):
    '''
    이미지 다운로드
    '''
    img_r = []
    for i, j in zip(img_urls, img_codes):
        if not os.path.exists(img_down_route+j+'.jpg'):
            request.urlretrieve(i, img_down_route+j+'.jpg')
        img_r.append(img_down_route+j+'.jpg')
            
    return img_r

def item_code_extraction(tyr_extraction_urls):
    '''
    상품코드 추출
    '''
    slash_num = 0
    ext_i_codes = []
    tmp = ''
    for i in tyr_extraction_urls:
        for j in i:
            if j == '/':
                slash_num += 1
            else:
                if slash_num == 5:
                    if j == '.':
                        ext_i_codes.append(tmp)
                        tmp = ''
                        slash_num = 0
                        break
                    else :
                        tmp += j
    return ext_i_codes

def category_item_code(top_item_urls, c_name):
    '''
    카테고리별 상위 11개 상품 정보 획득
    selenium 
    '''
    item_link = []
    img_link = []
    item_name = []
    img_tmp = ''
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument('--start-fullscreen')
        driver = webdriver.Chrome(options=options)
        driver.get(top_item_urls)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        # driver.save_screenshot(screenshot_name+'123'+'.png')
        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, 'html.parser') #URL과 파라메터 합쳐서 전달후 정보 읽어옴
        # soup = soup.find('div',class_ = 'top-ranking')
        # print(soup)rankings-item
        one_pic = soup.findAll('ul',class_='rankings-list')[0]
        one_pic = one_pic.find('li',class_='rankings-item')

        top_ten = soup.findAll('ul',class_='rankings-list')[1]
        soup = top_ten.findAll('li',class_='rankings-item')

        # print(len(soup))
        item_name.append(one_pic.find('div',class_='title').text)
        img_tmp = 'https:'+one_pic.find('img',class_='image').get('src')[:-12]
        if img_tmp[-1] == '_':
            img_link.append(img_tmp[:-1])
        else:
            img_link.append(img_tmp)
        item_link.append('https:'+one_pic.find('a').attrs['href'])

        for i in soup:
            item_name.append(i.find('div',class_='title').text)
            img_tmp = 'https:'+i.find('img',class_='image').get('src')[:-12]
            if img_tmp[-1] == '_':
                img_link.append(img_tmp[:-1])
            else:
                img_link.append(img_tmp)
            item_link.append('https:'+i.find('a').attrs['href'])

        return item_name, item_link, img_link
    except :
        return [], [], []

#div (title, ) img (image,(src)), a(href)

    
        
def top_category(top_rank_url):
    '''
    top_9 카테고리 url 획득 
    '''
    top_url = []
    top_name = []
    try : 
        requ = (top_rank_url)
        response_body = request.urlopen(requ).read()
        soup = (BeautifulSoup(response_body, 'html.parser')) #URL과 파라메터 합쳐서 전달후 정보 읽어옴
        ul_c = soup.find('div', class_='ui-slidebox-wrap') #필요한 부분 자름
        top_div = ul_c.findAll('div', class_='ui-slidebox-item')
        for i in top_div:
            top_str = 'https:'+i.find('a').attrs['href']
            top_name = (i.find('div', class_='product-name').text).split()
            top_url.append([top_str[:28]+'ko/__pc/'+top_str[28:], '_'.join(top_name)]) #url만 가공하여 습득
    except :
        return []

    return top_url#, top_name

def main():
    item_codes = []
    category_names = []
    top_lists = top_category(url)

    for i in range(len(top_lists)) :
        category_names.append(top_lists[i][1])
        top_lists[i] = top_lists[i][0]
        if '&' in category_names[i]:
            for j in range(len(category_names[i])):
                if category_names[i][j] == '&':
                    category_names[i] = category_names[i][:j]+'n'+category_names[i][j+1:]

    excel_create(top_lists, category_names) 
    
main() 
