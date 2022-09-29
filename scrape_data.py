import sys
import time
import logging
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException




class Goodreadscraper():

    def __init__(self,id,book_name):
        self.book_name=book_name
        self.page_count= 0
        print('----SETTING UP CHROME DRIVER----')
        try:
            print(f'----GETTING PAGE FOR {book_name} BOOK -----')
            self.url = f'https://www.goodreads.com/book/show/{id}.{book_name}'

            self.chromeoption = webdriver.ChromeOptions()
            self.chromeoption.add_experimental_option('excludeSwitches',
                                                      ['enable-automation'])
            self.chromeoption.add_argument("userAgent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/101.0.4951.44 Mobile/15E148 Safari/604.1")

            self.driver = webdriver.Chrome(options=self.chromeoption)
            agent = self.driver.execute_script("return navigator.userAgent")
            print('---THE AGENT IS',agent)
        except NoSuchWindowException:
            logging.warning('WINDOW DOES NOT EXIT')
            sys.exit()





    def scrape(self):

        self.driver.get(self.url)
        self.driver.implicitly_wait(220)
        time.sleep(5)
        close_popup_button=self.driver.find_element(By.CSS_SELECTOR,'i.Icon.CloseIcon')
        self.driver.execute_script("arguments[0].click();", close_popup_button)

        self.scroll_to_bottom_of_page()
        # self.scrape_data()
        # self.click_more_review_button()



    def scrape_data(self):

        book_review_data = {
            "reviewer_name": [],
            "reviewer_stats": [],
            "reviewer_ratings": [],
            "review_text_likes": [],
            "review_text": [],
        }

        print('-------scraping data-----')
        time.sleep(10)
        if self.page_count == 0 :
            # reviewer_name = self.driver.find_elements(By.CLASS_NAME,
            #                                           'ReviewerProfile__name')
            # reviewer_stats = self.driver.find_elements(By.CLASS_NAME,
            #                                            'ReviewerProfile__meta')
            # raw_reviewer_ratings = self.driver.find_elements(By.CSS_SELECTOR,
            #                                                  'div.ShelfStatus')
            # review_text_likes = self.driver.find_elements(By.CSS_SELECTOR,
            #                                               'div.SocialFooter__statsContainer')
            review_text = self.driver.find_elements(By.CSS_SELECTOR,
                                                    '#ReviewsSection .Formatted')
            # raw_reviewer_ratings = self.driver.find_elements(By.CSS_SELECTOR,
            #                                                  'div.ShelfStatus')
            #
            # clean_reviewer_ratings = []
            # for raw_ratings in raw_reviewer_ratings:
            #     new_ratings = raw_ratings.find_elements(By.CSS_SELECTOR, 'span.RatingStars.RatingStars__small')
            #     for clean_ratings in new_ratings:
            #         clean_reviewer_ratings.append(clean_ratings)


            for review in review_text:
                print(review.text)
        elif self.page_count == 1:
            review_text = self.driver.find_elements(By.CLASS_NAME,
                                                    'Formatted')
            for review in review_text:
                print(review.text)

        #
        # print('----ADDING TO DICTIONARY----')
        # for (name, stats, ratings, text_likes, reviewer_comment) in zip(reviewer_name, reviewer_stats,
        #                                                                 clean_reviewer_ratings, review_text_likes,
        #                                                                 review_text):
        #     book_review_data["reviewer_name"].append(name.text)
        #     book_review_data["reviewer_stats"].append(stats.text)
        #     book_review_data["reviewer_ratings"].append(ratings.get_attribute('aria-label'))
        #     book_review_data["review_text_likes"].append(text_likes.text)
        #     book_review_data["review_text"].append(reviewer_comment.text)

        print(f'-------DONE SCRAPING DATA FOR THE {self.page_count} PAGE')
        # df = pd.DataFrame(book_review_data)
        # self.append_data_to_file(self.book_name, df)

    def scroll_to_bottom_of_page(self):
        print('------SCROLLING TO THE BOTTOM OF THE PAGE-----')
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            current_height = self.driver.execute_script("return document.body.scrollHeight")

            if current_height == last_height and self.page_count == 0:
                print('------ DONE SCROLLING TO THE BOTTOM OF FIRST PAGE-----')
                time.sleep(5)
                self.scrape_data()
                self.click_more_review_button()
                break
            elif current_height == last_height and self.page_count == 1:
                time.sleep(5)
                self.scrape_data()
                self.click_more_review_button()
            last_height = current_height
        print('------ DONE SCROLLING TO THE BOTTOM OF THE PAGE-----')


    def click_more_review_button(self):
        if self.page_count == 0:
            print('-------CLICKING ON MORE REVIEW BUTTON-----')
            # self.driver.execute_script("arguments[0].scrollIntoView();", next_review_button)
            time.sleep(5)
            print('clicking more review button')
            next_review_button = self.driver.find_element(By.XPATH,
                                                          '//*[@id="ReviewsSection"]/div[5]/div/div[4]/a/span[1]')
            self.driver.execute_script("arguments[0].click();", next_review_button)


            self.url=self.driver.current_url
            self.page_count+=1
            print('----NOW NEW URL IS -----: ', self.url)
            print('-----REFRESHING DRIVER-----')
            self.driver.refresh()
            time.sleep(5)
            self.scroll_to_bottom_of_page()
            time.sleep(5)
        elif self.page_count == 1:
            # print('--------PRINTING PAGE SOURCE-------')
            # print(self.driver.page_source)
            print('clicking more review button')
            time.sleep(5)
            show_more_review_button = self.driver.find_element(By.XPATH,
                                                          '//*[@id="__next"]/div/main/div[1]/div[2]/div[4]/div[5]/div/button')

            self.driver.execute_script("arguments[0].click();", show_more_review_button)
            print('----CLICKING ON MORE REVIEWS----')
            self.scroll_to_bottom_of_page()


    def append_data_to_file(self,book_Name,dict):
        print('appending data to files')
        # with open(f'{book_Name}.json', 'w') as json_file:
        #     json.dump(dict, json_file)
        #     json_file.close()
        # dict.to_csv(f'{book_Name}.CSV',mode='a')
        time.sleep(5)
