import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
from io import StringIO

def fetch_nhl_2024_stats():
    url = "https://www.hockey-reference.com/leagues/NHL_2025.html"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    def get_table_by_id(table_id):
        #Extracts a table by ID from the main HTML.
        table = soup.find("table", id=table_id)
        if table is None:
            raise RuntimeError(f"Main HTML table with id '{table_id}' not found")
        df = pd.read_html(StringIO(str(table)))[0]
        df = df[~(df == list(df.columns)).all(axis=1)]
        df.reset_index(drop=True, inplace=True)
        return df

    def get_commented_table_by_id(table_id):
        #Extracts a table from within HTML comments
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment_soup = BeautifulSoup(comment, "html.parser")
            table = comment_soup.find("table", id=table_id)
            if table:
                df = pd.read_html(StringIO(str(table)))[0]
                df = df[~(df == list(df.columns)).all(axis=1)]
                df.reset_index(drop=True, inplace=True)
                return df
        raise RuntimeError(f"Commented table with id '{table_id}' not found")

    # Scrape each of the required tables
    stats = get_commented_table_by_id("stats")
    stats_adv = get_commented_table_by_id("stats_adv")
    standings_eas = get_table_by_id("standings_EAS")
    standings_wes = get_table_by_id("standings_WES")

    return stats, stats_adv, standings_eas, standings_wes

if __name__ == "__main__":
    stats, stats_adv, eas, wes = fetch_nhl_2024_stats()

    print("=== Basic Stats ===")
    print(stats.head())

    print("\n=== Advanced Stats ===")
    print(stats_adv.head())

    print("\n=== Eastern Conference Standings ===")
    print(eas.head())

    print("\n=== Western Conference Standings ===")
    print(wes.head())

    # Optional: Save to CSV
    stats.to_csv("nhl_2025_stats.csv", index=False)
    stats_adv.to_csv("nhl_2025_stats_five_on_five.csv", index=False)
    eas.to_csv("nhl_2025_east_standings.csv", index=False)
    wes.to_csv("nhl_2025_west_standings.csv", index=False)
