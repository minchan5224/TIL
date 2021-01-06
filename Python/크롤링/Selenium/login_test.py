from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys

start_url = 'https://login.aliexpress.com/buyer.htm?spm=2114.best.1000002.4.2fe5NYviNYviV9&return=https%3A%2F%2Fbest.aliexpress.com%2F%3Flan%3Den%26spm%3Da2g0s.buyerloginandregister.0.0.509c55a3Yemxat&from=lighthouse&random=119478436E545349111FABAB4D2473DA'
# 위의 url로 접속시 로그인 버튼 클릭할 필요가 없어진다.
screenshot_name = './screenshot/test_'
u_id = '' # 아이디
u_pw = '' # 비번 

def login_test():
  '''
  알리익스프레스 로그인 예시
  ID 필드와 PW 필드에 값을 넣은후 Keys.RETURN을 통해 로그인
  '''
  
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument('--start-fullscreen')
    
    

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
    driver.quit()

login_test()

