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



driver=webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.goodreads.com/book/show/19083.Politics')

soup=BeautifulSoup(driver.page_source,'html.parser')

ratings=soup.find_all('span',class_='staticStars notranslate')
print(len(ratings))

count =0 
empty=''
try:
        for y in ratings:
                if len(y.text):
                    print(y.text)
                    print('----')
                    count+=1
                else:
                    print('EMPTYYYYY')
except:
        print('NO RATINGS GIVEN')

print('THE AMOUNT IS : ' , count)
