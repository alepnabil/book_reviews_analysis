from scraper import Goodreadscraper
from s3_function import upload_to_s3


def collect_data():
    scraper=Goodreadscraper('https://www.goodreads.com/book/show/28862.The_Prince?from_search=true&from_srp=true&qid=ChhooCwVFc&rank=5', 'The prince', 'english')
    scraper.navigate_first_page()
    scraper.scrape_second_page()

    upload_to_s3('raw_data')


collect_data()
