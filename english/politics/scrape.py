import pandas as pd
from os import link, name
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
import time
import os

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager



class Scrape():

    #set our attributes as private attributes
    def __init__(self,path,link):
        self.path=path
        self.driver=webdriver.Chrome(self.path)
        self.link=link
    
    #to test request page
    def get_request(self):
        print('-----GETTING REQUEST------')
        try:
            time.sleep(2)
            self.driver.get(self.link)
            time.sleep(2)
        except:
            print('COULD NOT REQUEST PAGE')

class Reviews(Scrape):


    #get usernames of all users
    def get_usernames(self,source):
        self.soup=BeautifulSoup(source,"html.parser")
        time.sleep(2)
        username=self.soup.find_all('a',class_='user')
        Username=[user.text for user in username]
        print(f'----FOUND {len(username)} USERS-----')

        #check all the user's username
        for user in username:
            print(user.text)
        return Username
        

    def get_reviews(self):
        final_review=[]
        time.sleep(2)
        #doesnt get all the reviews(the short ones), cannot get the short reviews since the short reviews is not under span.readbale
        #reviews_body=self.soup.select('div#reviews span.readable [style="display:none"]')
        #navigate to review body
        reviews_body=self.soup.find_all('div',class_='reviewText stacked')
        #navigate to each review body
        for review in reviews_body:
            #in each body there will be 2 types of reviews (shorter and longer)
            #so we want to take the longer version
            words=review.find_all('span')
            #get the clean text
            clean_review=[review.text for review in words]
            #split both short and long reviews and get the longest review for each users
            temp_review=clean_review[0].split('\n',2)
            longest_review=(max(temp_review,key=len))
            final_review.append(longest_review)
            print(longest_review)
            print('-------------------------------------------------------------------')

        #supposedly there should be 30 reviews
        print(f'---------------FOUND {len(final_review)} REVIEWS---------------')
        return final_review

    def get_star_review(self):
      print('---GETTING STAR REVIEWS---')
      time.sleep(2)
      star=self.soup.select('span.staticStars.notranslate')
      Star=[review.text for review in star]
      #remove empty strings in the list
      while('' in Star):
          Star.remove('')

      print(Star)
      print(f'FOUND {len(Star)} STAR REVIEWS')
      for x in star:
          print(x.text)
          print('---------')
            
class Next_page(Reviews):

    def navigate_through_page(self):

        #go to first page
        print('getting page 1...')
        self.driver.get(self.link)
        source=self.driver.page_source
        #scrape first page usernames
        self.get_usernames(source)
        for i in range(2,11):
            try:
                print(f'getting page {i} ....') 
                time.sleep(7)
                #click on the next page button
                next_page=self.driver.find_element_by_class_name('next_page')
                next_page.click()
                time.sleep(7)
                #parse the elements of the new page (since it is on the same link)
                source=self.driver.page_source
                self.get_usernames(source)
            except:
                print('COULDNT CLICK')

main_page=Next_page(ChromeDriverManager().install(),'https://www.goodreads.com/book/show/19083.Politics')
#call the main function to get request from main page, if we dont call the main page requester our soup object wont be pass
#main_page.get_request()
#main_page.get_usernames()
#main_page.get_reviews()
#main_page.get_star_review()

main_page.navigate_through_page()