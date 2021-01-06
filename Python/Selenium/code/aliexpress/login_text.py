from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys

start_url = 'https://login.aliexpress.com/buyer.htm?spm=2114.best.1000002.4.2fe5NYviNYviV9&return=https%3A%2F%2Fbest.aliexpress.com%2F%3Flan%3Den%26spm%3Da2g0s.buyerloginandregister.0.0.509c55a3Yemxat&from=lighthouse&random=119478436E545349111FABAB4D2473DA'
screenshot_name = './screenshot/test_'
u_id = '' # 아이디
u_pw = '' # 비번

  
def item_search(sel_driver, item_codes):
    tmp = 0
    for i in item_codes:
        search_box = sel_driver.find_element_by_css_selector("input#search-key")
        search_box.send_keys(i)
        tmp += 1
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)
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
    pw_box.send_keys(Keys.RETURN)
    time.sleep(2)
    
    item_search(driver, lode_i_code)
    
    driver.quit()

main()
# test_tt()
#ui-slidebox-wrap
