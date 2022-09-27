import sys
import time
import logging
import json
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException




class Goodreadscraper():

    def __init__(self,id,book_name):
        self.book_name=book_name
        print('----SETTING UP CHROME DRIVER----')
        try:
            print(f'----GETTING PAGE FOR {book_name} BOOK -----')
            self.url = f'https://www.goodreads.com/book/show/{id}.{book_name}'

            self.chromeoption = webdriver.ChromeOptions()
            self.chromeoption.add_experimental_option('excludeSwitches',
                                                      ['enable-automation'])
            self.chromeoption.add_argument("userAgent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/101.0.4951.44 Mobile/15E148 Safari/604.1")

            self.driver = webdriver.Chrome(options=self.chromeoption)
        except NoSuchWindowException:
            logging.warning('WINDOW DOES NOT EXIT')
            sys.exit()


    def scrape(self):


        data=[]


        #define chromeoption
        self.driver=webdriver.Chrome(options=self.chromeoption)
        self.driver.get(self.url)
        self.driver.implicitly_wait(300)



        last_height=self.driver.execute_script("return document.body.scrollHeight")
        while True:
              self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
              time.sleep(3)
              current_height=self.driver.execute_script("return document.body.scrollHeight")


              if current_height == last_height:
                  reviewer_info = self.driver.find_elements(By.CLASS_NAME,
                                                            'TruncatedContent__text.TruncatedContent__text--large')


                  for review in reviewer_info:
                      review_dict={
                          "review_text":review.text
                      }
                      data.append(review_dict)


                  self.append_data_to_file(self.book_name,data)

                  print('value of data collected', len(data))
                  print('--at bottom page--')
                  self.click_more_review_button()
                  break
              last_height = current_height

    def click_more_review_button(self):
        print('clicking next page')
        more_review_button = self.driver.find_element(By.XPATH,
                                                      '//*[@id="ReviewsSection"]/div[5]/div/div[4]/a')
        self.driver.execute_script("arguments[0].click();", more_review_button)
        time.sleep(10000)


    def append_data_to_file(self,book_Name,dict):
        print('appending data to files')
        with open(f'{book_Name}.json', 'w') as json_file:
            json.dump(dict, json_file)
            json_file.close()

