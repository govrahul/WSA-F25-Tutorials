import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

def fetch_josh_allen_2024_gamelogs():
    url = "https://www.pro-football-reference.com/players/A/AlleJo02/gamelog/2024/"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    def get_table_by_id(table_id):
        table = soup.find("table", id=table_id)
        if table is None:
            raise RuntimeError(f"Table with id '{table_id}' not found")
        df = pd.read_html(StringIO(str(table)))[0]
        # Remove repeated header rows if any
        df = df[~(df == list(df.columns)).all(axis=1)]
        df.reset_index(drop=True, inplace=True)
        return df

    regular_season = get_table_by_id("stats")
    playoffs = get_table_by_id("stats_playoffs")

    return regular_season, playoffs

if __name__ == "__main__":
    regular_season_df, playoffs_df = fetch_josh_allen_2024_gamelogs()

    print("=== 2024 Regular Season ===")
    print(regular_season_df.head())

    print("\n=== 2024 Playoffs ===")
    print(playoffs_df.head())

    # Optional: Save to CSV
    regular_season_df.to_csv("josh_allen_2024_regular_season.csv", index=False)
    playoffs_df.to_csv("josh_allen_2024_playoffs.csv", index=False)
