import time
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()


class Goodreadscraper():
    """
    Scraper that will navigate to 2 pages on Goodreads to scrape book reviews

    """

    def __init__(self, url: str, book_name: str, language: str):

        self.url = url
        self.book_name = book_name
        self.page_count = 1
        self.language = language
        self.chromeoption = webdriver.ChromeOptions()
        self.chromeoption.add_experimental_option('excludeSwitches',
                                                  ['enable-automation'])
        self.chromeoption.add_argument(
            "userAgent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
            "like Gecko) CriOS/101.0.4951.44 Mobile/15E148 Safari/604.1")

        self.driver = webdriver.Chrome(options=self.chromeoption)
        self.driver.get(self.url)

        logging.basicConfig(filename="logs2.txt",
                            level=logging.DEBUG,
                            format='%(asctime)s %(message)s',
                            filemode='a')
        self.logger = logging.getLogger()

    def close_popup_button(self) -> None:

        """
        Closes the popup button when we access the webpage
        """
        try:
            self.logger.info('--CLICKING ON POPUP BUTTON--')
            # find the close popup button and click it
            close_popup_button = self.driver.find_element(By.CSS_SELECTOR, 'i.Icon.CloseIcon')
            self.driver.execute_script("arguments[0].click();", close_popup_button)
        except NoSuchElementException:
            self.logger.info('--POP UP BUTTON NOT AVAILABLE--')
            pass
        except ElementNotInteractableException:
            self.logger.info('--POP UP BUTTON CANNOT BE CLICKED--')
            pass

        time.sleep(3)
        try:
            remove_english_filter_button = self.driver.find_element(By.CSS_SELECTOR, 'I.Icon.XCircleIcon')
            self.driver.execute_script("arguments[0].click();", remove_english_filter_button)
        except NoSuchElementException:
            self.logger.info('--ENGLISH FILTER BUTTON NOT AVAILABLE--')
            pass
        except ElementNotInteractableException:
            self.logger.info('--ENGLISH FILTER CANNOT BE CLICKED--')
            pass

    def scroll_to_bottom_of_page(self) -> None:
        """
          Scrolls to the very bottom of the page to webscrape data.

          Will keep scrolling unless reaches the bottom of the webpage.

          If on page 1,it will scroll to the bottom of the page and scrape all data. Then click on the
          'More reviews and ratings' button.

          If on page 2, then it will keep scrolling to the very bottom of the page and scrape all data.
        """

        self.logger.info('------SCROLLING TO THE BOTTOM OF THE PAGE-----')
        # get the initial height of page
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        # keep scrolling to the bottom of the page
        while True:
            # scroll to the bottom of the page to render more content, hence increasing page height
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            # get the current height of page
            current_height = self.driver.execute_script("return document.body.scrollHeight")

            # if at the bottom of the page and on page 1
            if current_height == last_height and self.page_count == 1:
                self.logger.info(f'------ DONE SCROLLING TO THE BOTTOM OF THE {self.page_count} PAGE-----')
                time.sleep(5)
                break
            # if at the bottom of the page and on page 2
            elif current_height == last_height and self.page_count == 2:
                # try clicking on 'Show more reviews' button
                try:
                    time.sleep(5)
                    self.click_more_review_button()
                # if button is not available means at the very bottom of the page
                except:
                    self.logger.info(f'------ DONE SCROLLING TO THE BOTTOM OF {self.page_count} PAGE-----')
                    time.sleep(5)
                    break
            last_height = current_height

    def click_more_review_button(self) -> None:
        """
         On page 1, function will click on 'More reviews and ratings' button.
         Then it will navigate to page 2.

         On page 2, function will click on 'Show more reviews' button.
         Then it will continuously scroll to the bottom of the page.
         """

        if self.page_count == 1:
            self.logger.info('-------CLICKING ON MORE REVIEW BUTTON-----')
            time.sleep(5)
            next_review_button = self.driver.find_element(By.XPATH,
                                                          '//*[@id="ReviewsSection"]/div[5]/div/div[4]/a/span[1]')
            self.driver.execute_script("arguments[0].click();", next_review_button)

            self.url = self.driver.current_url
            self.page_count += 1
            time.sleep(5)
        elif self.page_count == 2:
            self.logger.info('-------CLICKING ON MORE REVIEW BUTTON-----')

            time.sleep(5)
            show_more_review_button = self.driver.find_element(By.CSS_SELECTOR,
                                                               'button.Button.Button--secondary.Button--small')

            self.driver.execute_script("arguments[0].click();", show_more_review_button)
            self.logger.info('----CLICKING ON MORE REVIEWS----')

    def scrape_data(self) -> None:

        """
        Scrapes relevant data such as reviewer's name, reviewer's stats, reviewer's rating,
        and reviewer comment likes.

        :Returns:
            Pandas dataframe
        """

        self.logger.info('--SCRAPING DATA--')
        book_author = self.driver.find_element(By.CLASS_NAME,
                                               'ContributorLink__name')
        book_author=book_author.text

        # on the first and second page, the reviews have different selector
        if self.page_count == 1:
            review_text = self.driver.find_elements(By.CSS_SELECTOR,
                                                    '#ReviewsSection .Formatted')
        elif self.page_count == 2:
            review_text = self.driver.find_elements(By.CLASS_NAME,
                                                    'Formatted')

        # get relevant data
        reviewer_name = self.driver.find_elements(By.CLASS_NAME,
                                                  'ReviewerProfile__name')
        reviewer_stats = self.driver.find_elements(By.CLASS_NAME,
                                                   'ReviewerProfile__meta')
        reviewer_ratings_div = self.driver.find_elements(By.CSS_SELECTOR,
                                                         'div.ShelfStatus')
        review_text_like_div = self.driver.find_elements(By.CSS_SELECTOR,
                                                         'section.ReviewCard__content')

        # handle nan values for ratings given
        reviewer_ratings = []
        for ratings in reviewer_ratings_div:
            try:
                stars = ratings.find_element(By.CSS_SELECTOR, 'span.RatingStars.RatingStars__small')
                stars_given = stars.get_attribute('aria-label')
                reviewer_ratings.append(stars_given)
            except:
                self.logger.info('--stars not given--')
                reviewer_ratings.append('None')
                pass

        # handle nan values for reviews that doesnt have likes
        review_text_like = []
        for like in review_text_like_div:
            try:
                comment_like = like.find_element(By.CSS_SELECTOR,
                                                 'div.SocialFooter__statsContainer')
                comment_like = comment_like.text
                review_text_like.append(comment_like)
            except:
                review_text_like.append('None')
                self.logger.info('likes not given')
                pass

        reviewer_name = list(map(lambda name: name.text, reviewer_name))
        review_text = list(map(lambda text: text.text, review_text))
        reviewer_stats = list(map(lambda stats: stats.text, reviewer_stats))
        data = pd.DataFrame(zip(reviewer_name, review_text, reviewer_stats, reviewer_ratings, review_text_like),
                            columns=['name', 'review', 'reviewer_stats', 'ratings_given', 'review_like'])
        data['book_author'] = book_author
        # save data to csv
        self.save_data(data)

    def save_data(self, data: pd.DataFrame) -> None:
        """
        Save data to csv
        :param data: Pandas dataframe

        """
        if self.page_count == 1:
            data.to_csv(f'raw_data/{self.language}/{self.book_name}.csv', mode='a', index=False, encoding='utf-8')
        elif self.page_count == 2:
            data.to_csv(f'raw_data/{self.language}/{self.book_name}.csv', mode='a', index=False, header=False,
                        encoding='utf-8')

        self.logger.info('---DONE SAVING TO CSV--')

    def scrape_first_page(self):
        self.close_popup_button()
        self.scroll_to_bottom_of_page()
        self.scrape_data()
        self.click_more_review_button()

    def scrape_second_page(self):
        self.close_popup_button()
        self.scroll_to_bottom_of_page()
        self.scrape_data()
