import requests
from bs4 import BeautifulSoup, Comment

url = "https://www.basketball-reference.com/teams/DET/stats_basic_yr_yr.html"
resp = requests.get(url)
soup = BeautifulSoup(resp.text, "html.parser")

def print_tables_info(tables, source):
    print(f"\nTables found in {source}: {len(tables)}\n")
    for i, table in enumerate(tables):
        table_id = table.get("id", "No ID")
        caption = table.find("caption")
        caption_text = caption.text.strip() if caption else "No caption"
        print(f"[{source} Table {i}] id: {table_id}, caption: {caption_text}")

# 1. Tables in main HTML
main_tables = soup.find_all("table")
print_tables_info(main_tables, "main HTML")

# 2. Tables inside comments
comments = soup.find_all(string=lambda text: isinstance(text, Comment))
comment_tables = []
for comment in comments:
    comment_soup = BeautifulSoup(comment, "html.parser")
    comment_tables.extend(comment_soup.find_all("table"))

print_tables_info(comment_tables, "comments")
