import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

class F1Scraper:
    # constants
    DOMAIN = 'https://www.formula1.com'
    RACES_URL = DOMAIN + '/en/results/{}/races'
    DRIVERS_URL = DOMAIN + '/en/results/{}/drivers'

    def __init__(self):
        self.session = requests.session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
        })
        self.df_list_races = []
        self.df_list_drivers = []
        self.df_list_results = []

    # scrapers
    def get_races(self, year):
        r = self.session.get(self.RACES_URL.format(year))
        r.raise_for_status()
        soup = bs(r.content, 'html.parser')
        for row in soup.select('#results-table table > tbody > tr'):
            _data = {
                'year': year,
                'grand_prix': str(row.select_one('td:nth-child(1) > a').find(string=True, recursive=False)),
                'url': self.DOMAIN + row.select_one('td:nth-child(1) > a').get('href'),
                'date': row.select_one('td:nth-child(2)').get_text(strip=True),
                'winner_driver_first_name': row.select_one('td:nth-child(3) span[class="max-lg:hidden"]').get_text(strip=True),
                'winner_driver_last_name': row.select_one('td:nth-child(3) span[class="max-md:hidden"]').get_text(strip=True),
                'winner_driver_short_name': row.select_one('td:nth-child(3) span[class="md:hidden"]').get_text(strip=True),
                'winner_team': row.select_one('td:nth-child(4)').get_text(strip=True),
                'winner_laps': row.select_one('td:nth-child(5)').get_text(strip=True),
                'winner_time': row.select_one('td:nth-child(6)').get_text(strip=True),
            }
            self.df_list_races.append(_data)

    def get_drivers(self, year):
        r = self.session.get(self.DRIVERS_URL.format(year))
        r.raise_for_status()
        soup = bs(r.content, 'html.parser')
        for row in soup.select('#results-table table > tbody > tr'):
            _data = {
                'year': year,
                'pos': row.select_one('td:nth-child(1)').get_text(strip=True),
                'first_name': row.select_one('td:nth-child(2) span[class="max-lg:hidden"]').get_text(strip=True),
                'last_name': row.select_one('td:nth-child(2) span[class="max-md:hidden"]').get_text(strip=True),
                'short_name': row.select_one('td:nth-child(2) span[class="md:hidden"]').get_text(strip=True),
                'url': self.DOMAIN + row.select_one('td:nth-child(2) > a').get('href'),
                'nationality': row.select_one('td:nth-child(3)').get_text(strip=True),
                'team': row.select_one('td:nth-child(4) > a').get_text(strip=True),
                'team_url': self.DOMAIN + row.select_one('td:nth-child(4) > a').get('href'),
                'pts': row.select_one('td:nth-child(5)').get_text(strip=True),
            }
            self.df_list_drivers.append(_data)

    def get_results(self, race_url):
        r = self.session.get(race_url)
        r.raise_for_status()
        soup = bs(r.content, 'html.parser')
        for row in soup.select('#results-table table > tbody > tr'):
            _data = {
                'url': race_url,
                'po': row.select_one('td:nth-child(1)').get_text(strip=True),
                'no': row.select_one('td:nth-child(2)').get_text(strip=True),
                'driver_first_name': row.select_one('td:nth-child(3) span[class="max-lg:hidden"]').get_text(strip=True),
                'driver_last_name': row.select_one('td:nth-child(3) span[class="max-md:hidden"]').get_text(strip=True),
                'driver_short_name': row.select_one('td:nth-child(3) span[class="md:hidden"]').get_text(strip=True),
                'team': row.select_one('td:nth-child(4)').get_text(strip=True),
                'laps': row.select_one('td:nth-child(5)').get_text(strip=True),
                'time': row.select_one('td:nth-child(6)').get_text(strip=True),
                'pts': row.select_one('td:nth-child(7)').get_text(strip=True),
            }
            self.df_list_results.append(_data)

    def scrape_all(self, years):
        # scraping
        print('get races')
        with ThreadPoolExecutor() as ex:
            list(tqdm(ex.map(self.get_races, years), total=len(years)))

        print('get drivers')
        with ThreadPoolExecutor() as ex:
            list(tqdm(ex.map(self.get_drivers, years), total=len(years)))

        print('get results')
        with ThreadPoolExecutor() as ex:
            list(tqdm(ex.map(self.get_results, [r['url'] for r in self.df_list_races]), total=len(self.df_list_races)))

        return (
            self.df_list_races, 
            self.df_list_drivers, 
            self.df_list_results,
        )

if __name__ == '__main__':
    scraper = F1Scraper()
    years = list(range(1950, 1960))
    races, drivers, results = scraper.scrape_all(years)

    pd.DataFrame(races).to_csv('./sample/races.csv', index=False)
    pd.DataFrame(drivers).to_csv('./sample/drivers.csv', index=False)
    pd.DataFrame(results).to_csv('./sample/results.csv', index=False)
