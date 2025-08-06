import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
from io import StringIO

def fetch_michigan_2024_schedule():
    url = "https://www.sports-reference.com/cfb/schools/michigan/2024-schedule.html"
    resp = requests.get(url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table", id="schedule")
    if table is None:
        raise RuntimeError("Could not find the schedule table on the page")

    # Use pandas to parse the HTML table
    df = pd.read_html(str(table))[0]
    # Clean up the DataFrame
    # Remove any header rows repeated inside
    df = df[df['G'] != 'G']
    # Reset index
    df = df.reset_index(drop=True)
    return df

def fetch_michigan_2024_stats():
    url = "https://www.sports-reference.com/cfb/schools/michigan/2024.html"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    def get_table_by_id(table_id):
        table = soup.find("table", id=table_id)
        if not table:
            raise RuntimeError(f"Table with id '{table_id}' not found")
        df = pd.read_html(StringIO(str(table)))[0]

        # Clean repeated header rows if any
        try:
            df = df[~(df == list(df.columns)).all(axis=1)]
        except Exception:
            pass
        df.reset_index(drop=True, inplace=True)
        return df

    team_stats = get_table_by_id("team")
    passing = get_table_by_id("passing_standard")
    rushing_receiving = get_table_by_id("rushing_standard")

    return team_stats, passing, rushing_receiving


if __name__ == "__main__":
    team_stats, passing, rushing_receiving = fetch_michigan_2024_stats()

    print("\n=== Team Stats ===")
    print(team_stats.head())
    print("\n=== Passing ===")
    print(passing.head())
    print("\n=== Rushing & Receiving ===")
    print(rushing_receiving.head())

    # Save to CSV
    team_stats.to_csv("michigan_2024_team_stats.csv", index=False)
    passing.to_csv("michigan_2024_passing.csv", index=False)
    rushing_receiving.to_csv("michigan_2024_rushing_receiving.csv", index=False)