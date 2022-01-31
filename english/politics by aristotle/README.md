
# Book reviews analysis

How can we determine an author is right? What do people have to say about certain books? Does only reading the book makes us understand it? Do we have the same opinion as others about books we read?
This is a book reviews sentiment analysis project in which the book reviews are scraped from different book review websites. After finishing a book, reviews about that book will be scraped to carry out analysis on other reader's opinions.
 

## Aim of project
- Apply constructivism learning by comparing other reader's reviewer.
- Carry out the sentiment analysis behind the doctrine that is being put forward by the author.

 
 
## Folder structure
| Scripts | Description |
| --- | ----------- |
| scrape.py | Extract and gather data by scraping from book review websites by using webscraping tools such as Beautifulsoup and Selenium |
| append_data.py | Load all gathered data into 1 csv file |
| df.csv | Unclean text data |
| data cleaning.ipynb| Cleaning raw text data by using multiple NLTK techniques such as stemming text data,lemmatizing text data,removing stop words, removing punctuation, and converting text to lower case|
| df_final.csv | Cleaned text data 
| eda_and_sentiment_analysis.ipynb | Carried out exploratory data analysis on reviews to gain insights and sentiment analysis to gain better undestanding of the books|

 
 
## Tech


**Language:** Python

**Libraries:** Requests,Pandas,Seaborn,Matplotlib,NLTK,Vader,Malaya,Textblob

**Web scraping:** Beautifulsoup,Selenium

**Books:** Natural Language Processing Recipes by Apress



  
