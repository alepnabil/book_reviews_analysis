import sys
import time
import logging
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import NoSuchElementException




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

            # book_review_data = {
            #     "reviewer_name": [],
            #     "reviewer_stats": [],
            #     "reviewer_ratings": [],
            #     "review_text": [],
            # }

            print('-------scraping data-----')

            # on the first and second page, the reviews have different selector
            if self.page_count == 0:
                review_text = self.driver.find_elements(By.CSS_SELECTOR,
                                                        '#ReviewsSection .Formatted')
            elif self.page_count == 1:
                review_text = self.driver.find_elements(By.CLASS_NAME,
                                                        'Formatted')

            reviewer_name = self.driver.find_elements(By.CLASS_NAME,
                                                              'ReviewerProfile__name')
            reviewer_stats = self.driver.find_elements(By.CLASS_NAME,
                                                               'ReviewerProfile__meta')
            reviewer_ratings_div = self.driver.find_elements(By.CSS_SELECTOR,
                                                                     'div.ShelfStatus')
            review_text_like_div=self.driver.find_elements(By.CSS_SELECTOR,
                                                           'section.ReviewCard__content')




            #to handle nan values for ratings given
            reviewer_ratings = []
            for ratings in reviewer_ratings_div:
                print('------')
                try:
                    stars=ratings.find_element(By.CSS_SELECTOR, 'span.RatingStars.RatingStars__small')
                    stars_given=stars.get_attribute('aria-label')
                    print(stars_given)
                    reviewer_ratings.append(stars_given)
                except:
                    print('---stars not given---')
                    reviewer_ratings.append('None')
                    pass

            #to handle nan values for reviews that doesnt have likes
            review_text_like=[]
            for like in review_text_like_div:
                try:
                    comment_like=like.find_element(By.CSS_SELECTOR,
                                                   'div.SocialFooter__statsContainer')
                    comment_like=comment_like.text
                    review_text_like.append(comment_like)
                    print(comment_like)
                except:
                    review_text_like.append('None')
                    print('none given')
                    pass




            reviewer_name=list(map(lambda name:name.text,reviewer_name))
            review_text=list(map(lambda text:text.text,review_text))
            reviewer_stats=list(map(lambda stats:stats.text,reviewer_stats))

            data=pd.DataFrame(zip(reviewer_name,review_text,reviewer_stats,reviewer_ratings,review_text_like),
                              columns=['name','review','reviewer_stats','ratings_given','review_like'])


            print(data)
            data.to_csv(f'{self.book_name}.CSV', mode='a',index=False)




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
        dict.to_csv(f'{book_Name}.CSV',mode='a')
        time.sleep(5)
