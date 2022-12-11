import pandas as pd
import time
from scraper import Scraper

if __name__ == '__main__':
    start_time = time.time()
    dfs = [pd.read_html(f'https://de.wikipedia.org/wiki/MDAX')[1], pd.read_html(f'https://de.wikipedia.org/wiki/TECDAX')[5], pd.read_html(f'https://de.wikipedia.org/wiki/DAX')[1], pd.read_html(f'https://de.wikipedia.org/wiki/SDAX')[2]]
    s = Scraper()
    for df in dfs:
        for v in df["Name"].values:
            print(f"Scraping {v}")
            s.download_company(v)
    s.close()
    print("--- %s seconds ---" % (time.time() - start_time))
