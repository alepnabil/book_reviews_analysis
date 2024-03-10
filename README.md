
# Book reviews analysis

This is a data engineering project where readers reviews from [Goodreads.com](https://www.goodreads.com/?ref=nav_hom) were scraped and sentiment analysis were performed. Collected raw scraped data were stored in a raw data AWS S3 bucket. Raw scraped data from S3 is then pulled and processed using libraries such as Pandas, Vader(sentiment analysis), Langdetect(Language classifier) and orchestrated using Apache Airflow. Clean data is then stored inside a clean data AWS S3 bucket. Clean data from S3 bucket is then loaded into AWS RDS using AWS Glue. Finally, clean and formatted data is visualized using Streamlit Cloud.

# Demo
![gif](https://user-images.githubusercontent.com/65908522/229330837-d8a1813e-1e99-41cd-b893-5567c5f21826.gif)


# DAG folder directory

| directory       | Details          |
| ------------- |:-------------:|
| dags/dag.py   | Main DAG containing Airflow orchestration.|
| dags/scrape_data.py   |Selenium and beautifulsoup web scraper.|
| dags/preprocess_data/process_data.py   | Process data such as getting author number of books, ratings given by reader etc. Contains data coversion and data validation functions.
| dags/preprocess_data/data_validation.py   | Contains data validation functions using Pandera.|
|dags/aws_functions   | Contains AWS functions to upload data to S3 and Redshift.|

# Visualization folder directory
| directory | Details|
| ------------- |:-------------:|
| webpage/main_page.py   |Contains SQL queries for main page visualization analysis and Plotly graphs.|
| webpage/indv_book_page.py   | Contains SQL queries for individual books visualization analysis.|



# Architechture
![final4 drawio](https://user-images.githubusercontent.com/65908522/229278332-a595922b-36ef-43b2-9b7d-8d1b58a5f9f9.png)
> *Click on image to view full image*

# Link to dashboard
https://bookreviewsentiment.streamlit.app/
> *(Link does not work all the time as connection to data warehouse requires app reboot.)*
 

# ETL

![image](https://user-images.githubusercontent.com/65908522/229275814-d0cb2fe3-2cbe-4016-8a5f-712c90a3dc06.png)



# Data warehouse
![data warehouse](https://user-images.githubusercontent.com/65908522/229277881-01c94def-b4ff-4f15-b4d4-a958e1bef75f.png)





  
