
# Book reviews analysis

This is a data engineering project where readers review from [Goodreads.com](https://www.goodreads.com/?ref=nav_hom) were scraped and sentiment analysis were performed. Collected raw scraped data were stored in a raw data AWS S3 bucket. Raw scraped data from S3 is then pulled and processed using libraries such as Pandas, Vader(sentiment analysis), Langdetect(Language classifier). Clean data is then stored inside a clean data AWS S3 bucket. Clean data from S3 bucket is then loaded into AWS RDS using AWS Glue. Finally, clean and formatted data is visualized using Streamlit Cloud.

# Architechture
![final2 drawio](https://user-images.githubusercontent.com/65908522/229276298-bab13e33-9883-4ebb-9003-aadfd485fea1.png)
> *Click on image to view full image*

# Link to dashboard
https://bookreviewsentiment.streamlit.app/
> *(Link does not work all the time as connection to data warehouse requires app reboot.)*
 


# ETL

![image](https://user-images.githubusercontent.com/65908522/229275814-d0cb2fe3-2cbe-4016-8a5f-712c90a3dc06.png)






  
