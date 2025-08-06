import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

def fetch_michigan_2024_schedule():
    url = "https://www.sports-reference.com/cbb/schools/michigan/men/2025-schedule.html"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Find the schedule table by id
    table = soup.find("table", id="schedule")
    if not table:
        raise RuntimeError("Schedule table not found")

    # Use StringIO to avoid FutureWarning
    df = pd.read_html(StringIO(str(table)))[0]

    # Only drop a level if MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel()

    # Example: filter out exhibition games (if needed)
    # if "Date" in df.columns:
    #   df = df[~df["Date"].str.contains("Exhibition", na=False)]

    df.reset_index(drop=True, inplace=True)

    return df


def fetch_team_stats_and_per_game():
    url = "https://www.sports-reference.com/cbb/schools/michigan/men/2025.html"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    def get_table_by_id(table_id):
        table = soup.find("table", id=table_id)
        if table is None:
            raise RuntimeError(f"Table with id '{table_id}' not found")
        df = pd.read_html(StringIO(str(table)))[0]
        # Remove repeated headers if any
        df = df[~(df == list(df.columns)).all(axis=1)]
        df.reset_index(drop=True, inplace=True)
        return df

    team_stats = get_table_by_id("season-total_totals")
    per_game = get_table_by_id("players_per_game")

    return team_stats, per_game

if __name__ == "__main__":
    team_stats_df, per_game_df = fetch_team_stats_and_per_game()

    print("=== Total Team and Opponent Stats ===")
    print(team_stats_df.head())

    print("\n=== Per Game Stats ===")
    print(per_game_df.head())

    # Save to CSV if you want
    team_stats_df.to_csv("michigan_2025_total_team_stats.csv", index=False)
    per_game_df.to_csv("michigan_2025_per_game_stats.csv", index=False)