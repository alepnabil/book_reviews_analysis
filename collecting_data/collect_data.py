from scraper import Goodreadscraper
from s3_function import upload_to_s3


def collect_data():
    scraper=Goodreadscraper('https://www.goodreads.com/book/show/448836.Second_Treatise_of_Government', 'Second treatise of government', 'english')
    scraper.navigate_first_page()
    scraper.scrape_second_page()

    upload_to_s3('raw_data')


collect_data()
