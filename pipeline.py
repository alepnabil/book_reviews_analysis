from scrape_data import Goodreadscraper

def main():
    scraper=Goodreadscraper('91953','Leviathan')
    scraper.scrape()


if __name__ == '__main__':
    main()