
# Book reviews analysis

This is a data engineering project where readers review from [Goodreads.com](https://www.goodreads.com/?ref=nav_hom) were scraped and sentiment analysis were performed. Collected raw scraped data were stored in a raw data AWS S3 bucket. Raw scraped data from S3 is then pulled and processed using libraries such as Pandas, Vader(sentiment analysis), Langdetect(Language classifier). Clean data is then stored inside a clean data AWS S3 bucket. Clean data from S3 bucket is then loaded into AWS RDS using AWS Glue. Finally, clean and formatted data is visualized using Streamlit Cloud.

# Architechture


# Link to dashboard
https://bookreviewsentiment.streamlit.app/
> *(Link does not work all the time as connection to data warehouse requires app reboot.)*
 
# Dashboard demo


 
 
# Folder structure
| Folder | Description |
| --- | ----------- |
| collecting_data | Scrape data using Selenium and Selenium Image from Docker |
| dags| ETL pipeline |
| webpage | Streamlit dashboard customization |


# ETL


# Data warehouse





  
