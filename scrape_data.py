import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


url='https://www.goodreads.com/book/show/91953.Leviathan'

chromeoption = webdriver.ChromeOptions()
chromeoption.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
chromeoption.add_experimental_option('excludeSwitches', ['enable-automation'])





driver=webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(220)
last_height=driver.execute_script("return document.body.scrollHeight")
while True:
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

      time.sleep(3)
      current_height=driver.execute_script("return document.body.scrollHeight")
      if current_height==last_height:
        break
      last_height=current_height

      # driver.find_elements(By.CLASS_NAME,'ReviewCard__content')

      reviewer_info=driver.find_elements(By.CLASS_NAME,'TruncatedContent__text.TruncatedContent__text--large')
      print(reviewer_info)
      for x in reviewer_info:
        print('-------')
        print(x.text)

