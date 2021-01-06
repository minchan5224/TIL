from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys

start_url = 'https://login.aliexpress.com/buyer.htm?spm=2114.best.1000002.4.2fe5NYviNYviV9&return=https%3A%2F%2Fbest.aliexpress.com%2F%3Flan%3Den%26spm%3Da2g0s.buyerloginandregister.0.0.509c55a3Yemxat&from=lighthouse&random=119478436E545349111FABAB4D2473DA'
screenshot_name = './screenshot/test_'
u_id = ''
u_pw = ''


# def test_tt():
#     test1 = 'https://sale.aliexpress.com/ko/__pc/rank_detail.htm?rankId=2554194&rankCategoryId=322&labelId=&leafCateId=&rankType=TOP_SALES&t'
#     test2 = 'agId=affi_toc_322&requestFrom=other&productIds2Top=4000470883084%252C4000220112045%252C4000189910894'
#     test3 = '&scm=1007.26693.176071.0&scm_id=1007.26693.176071.0&scm-url=1007.26693.176071.0&pvid=bd5b30be-3df0-452d-98bd-1599393ac650&floorId=9434523'

#     test = test1 + test2 + test3
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument('--start-fullscreen')
    
#     lode_i_code = ['4000519228140'] #test

#     driver = webdriver.Chrome(options=options)
    
#     driver.get('https://best.aliexpress.com/?lan=ko&spm=a2g0o.ams_97944.1000002.1.324fRhShRhShWo')
#     time.sleep(5)
#     driver.save_screenshot(screenshot_name+str(12333)+'.png')
#     driver.quit()

    
def item_search(sel_driver, item_codes):
    tmp = 0
    for i in item_codes:
        search_box = sel_driver.find_element_by_css_selector("input#search-key")
        search_box.send_keys(i)
        sel_driver.save_screenshot(screenshot_name+str(tmp)+'.png')
        tmp += 1
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)
        sel_driver.save_screenshot(screenshot_name+str(tmp)+'.png')
        print(sel_driver.current_url)#url 가져오기
        


def main():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument('--start-fullscreen')
    
    lode_i_code = ['4000519228140'] #test

    driver = webdriver.Chrome(options=options)
    
    driver.get(start_url)
    time.sleep(5)
    # driver.save_screenshot(screenshot_name+str(tmp)+'.png')
    id_box = driver.find_element_by_css_selector("input#fm-login-id")
    id_box.send_keys(u_id)
    pw_box = driver.find_element_by_css_selector("input#fm-login-password")
    pw_box.send_keys(u_pw)

    time.sleep(2)
    # driver.save_screenshot(screenshot_name+str(tmp)+'.png')
    pw_box.send_keys(Keys.RETURN)
    time.sleep(2)
    # driver.save_screenshot(screenshot_name+str(tmp)+'.png')
    
    item_search(driver, lode_i_code)
    
    driver.quit()

main()
# test_tt()
#ui-slidebox-wrap