import pandas as pd

from scraper import Scraper

if __name__ == '__main__':
    dfs = [pd.read_html(f'https://de.wikipedia.org/wiki/SDAX')[2], pd.read_html(f'https://de.wikipedia.org/wiki/MDAX')[1], pd.read_html(f'https://de.wikipedia.org/wiki/TECDAX')[5], pd.read_html(f'https://de.wikipedia.org/wiki/DAX')[1]]
    s = Scraper()
    for df in dfs:
        for v in df["Name"].values:
            print(f"Scraping {v}")
            s.download_company(v)
    s.close()
