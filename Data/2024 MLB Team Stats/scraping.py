import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
from io import StringIO

def fetch_mlb_stats():
    url = "https://www.baseball-reference.com/leagues/majors/2024.shtml"
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
    batting = get_table_by_id("teams_standard_batting")
    postseason = get_commented_table_by_id("postseason")
    pitching = get_commented_table_by_id("teams_standard_pitching")
    output = get_commented_table_by_id("team_output")
    fielding = get_commented_table_by_id("teams_standard_fielding")

    return batting, postseason, pitching, output, fielding

if __name__ == "__main__":
    batting, postseason, pitching, output, fielding = fetch_mlb_stats()

    print("=== Batting Stats ===")
    print(batting.head())

    print("\n=== Postseason Results ===")
    print(postseason.head())

    print("\n=== Wins Above Avg ===")
    print(output.head())

    print("\n=== Pitching Stats ===")
    print(pitching.head())

    print("\n=== Fielding Stats ===")
    print(fielding.head())

    # Optional: Save to CSV
    batting.to_csv("2024_batting.csv", index=False)
    postseason.to_csv("2024_postseason_results.csv", index=False)
    pitching.to_csv("2024_pitching.csv", index=False)
    output.to_csv("2024_wins_above_avg_by_position.csv", index=False)
    fielding.to_csv("2024_fielding.csv", index=False)