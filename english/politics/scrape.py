import pandas as pd
from os import link, name
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from openpyxl import Workbook,load_workbook
from openpyxl.utils import get_column_letter
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
        self.Username=Username
      
       
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
        User_reviews=final_review
        self.User_reviews=User_reviews

    def get_star_review(self,page):
      Star=[]
      print('---GETTING STAR REVIEWS---')
      time.sleep(2)
      div=self.soup.find_all('div',class_='reviewHeader uitext stacked')

      #find all the review divs
      for x in div:
        try:
            #try to see if the user gives a star review or not 
            print('FOUND STAR REVIEW')
            ratings=x.find('span',class_='staticStars notranslate')
            for y in ratings:
                #if there is a star review, we only want the review text
                #so this ignores the empty strings(?)
                #else will just pass
                if len(y.text):
                    print(y.text)
                    Star.append(y.text)
                    print('------------')
                else:
                    pass
        #if the user doesnt give any star review
        except:
            print('-------------COULDNT FIND ELEMENT----------------')
            Star.append('NONE')

      print(Star)
      print(f'FOUND {len(Star)} STAR REVIEWS')


      self.append_to_csv(self.Username, self.User_reviews, Star, page)


    def append_to_csv(self,username,user_reviews,star,page_name):

        print(f'appending to csv for page {page_name}....')
        
        
        Username=pd.DataFrame(username)
        User_reviews=pd.DataFrame(user_reviews)
        User_star=pd.DataFrame(star)

        df=pd.concat([Username,User_reviews,User_star],axis=1)
        df.to_csv('E:\\New folder\\Udemy\\personal data science projects\\book reviews analysis\\english\\politics\\data\\'+str(page_name)+'_page.csv')
        print(f'done saving csv for {page_name} page')

            
class Next_page(Reviews):

    def navigate_through_page(self):

        #go to first page
        print('getting page 1...')
        self.driver.get(self.link)
        source=self.driver.page_source

        #scrape first page usernames
        self.get_usernames(source)
        self.get_reviews()
        self.get_star_review(1)

        #loop through other pages. in this case we know there is 10 pages.
        for i in range(2,11):
            try:
                print(f'getting page {i} ....') 
                time.sleep(7)
                #currently we are still at the first page
                #now we click next page
                next_page=self.driver.find_element_by_class_name('next_page')
                next_page.click()
                #parse the elements of the new page (since it is on the same link)
                time.sleep(10)
                source=self.driver.page_source
                self.get_usernames(source)
                self.get_reviews()
                self.get_star_review(i)
            except:
                print('COULDNT CLICK')

main_page=Next_page(ChromeDriverManager().install(),'https://www.goodreads.com/book/show/19083.Politics')
#call the main function to get request from main page, if we dont call the main page requester our soup object wont be pass
#main_page.get_request()
#main_page.get_usernames()
#main_page.get_reviews()
#main_page.get_star_review()

main_page.navigate_through_page()