import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
from io import StringIO

def fetch_worldcup_2024_stats():
    url = "https://fbref.com/en/comps/1/World-Cup-Stats"
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
    stats = get_table_by_id("results202210_overall")

    return stats

if __name__ == "__main__":
    stats = fetch_worldcup_2024_stats()

    print("=== Basic Stats ===")
    print(stats.head())

    # Optional: Save to CSV
    stats.to_csv("world_cup_league_table.csv", index=False)
