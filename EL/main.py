from extract import F1Scraper
from load import saving

if __name__ == '__main__':
    scraper = F1Scraper()
    years = list(range(1950, 1960))
    df_races, df_drivers, df_results = scraper.scrape_all(years)
    saving(df_races, df_drivers, df_results)
