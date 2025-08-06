import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

def fetch_pistons_stats():
    url = "https://www.basketball-reference.com/teams/DET/stats_basic_yr_yr.html"
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

    stats = get_table_by_id("stats")

    return stats

if __name__ == "__main__":
    stats = fetch_pistons_stats()

    print("=== Pistons Year-over-Year Stats ===")
    print(stats.head())

    # Optional: Save to CSV
    stats.to_csv("Pistons_Opponent_Year_over_Year_Stats.csv", index=False)