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
    
    #request page 
    def get_request(self):
        print('-----GETTING REQUEST------')
        try:
            time.sleep(2)
            self.driver.get(self.link)
            time.sleep(2)
            self.soup=BeautifulSoup(self.driver.page_source,"html.parser")
        except:
            print('COULD NOT REQUEST PAGE')
    

class Reviews(Scrape):


    #get usernames of all users
    def get_usernames(self):
        time.sleep(2)
        username=self.soup.find_all('a',class_='user')
        print(f'----FOUND {len(username)} USERS REVIEWS-----')
        for user in username:
            print(user.text)

    def get_reviews(self):
        time.sleep(2)
        reviews=self.soup.find_all('')   

main_page=Reviews(ChromeDriverManager().install(),'https://www.goodreads.com/book/show/19083.Politics')
#call the main function to get request from main page, if we dont call the main page requester our soup object wont be pass
main_page.get_request()
main_page.get_usernames()