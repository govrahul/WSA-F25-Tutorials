import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

def fetch_lions_2024_gamelogs():
    url = "https://www.pro-football-reference.com/teams/det/2024.htm"
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

    games = get_table_by_id("games")
    team_stats = get_table_by_id("team_stats")
    passing = get_table_by_id("passing")
    passing_postseason = get_table_by_id("passing_post")
    rushing_receiving = get_table_by_id("rushing_and_receiving")
    rushing_receiving_postseason = get_table_by_id("rushing_and_receiving_post")

    return games, team_stats, passing, passing_postseason, rushing_receiving, rushing_receiving_postseason

if __name__ == "__main__":
    games, team_stats, passing, passing_postseason, rushing_receiving, rushing_receiving_postseason = fetch_lions_2024_gamelogs()

    print("=== 2024 Seasons ===")
    print(games.head())

    print("\n=== 2024 Team Stats ===")
    print(team_stats.head())

    print("\n=== 2024 Passing Stats ===")
    print(passing.head())

    print("\n=== 2024 Passing Playoffs Stats ===")
    print(passing_postseason.head())

    print("\n=== 2024 Rushing and Receiving Stats ===")
    print(rushing_receiving.head())

    print("\n=== 2024 Rushing and Receiving Playoffs Stats ===")
    print(rushing_receiving_postseason.head())

    # Optional: Save to CSV
    games.to_csv("lions_2024_season.csv", index=False)
    team_stats.to_csv("lions_2024_team_stats.csv", index=False)
    passing.to_csv("lions_2024_passing.csv", index=False)
    passing_postseason.to_csv("lions_2024_passing_playoffs.csv", index=False)
    rushing_receiving.to_csv("lions_2024_rushing_receiving.csv", index=False)
    rushing_receiving_postseason.to_csv("lions_2024_rushing_receiving_playoffs.csv", index=False)
