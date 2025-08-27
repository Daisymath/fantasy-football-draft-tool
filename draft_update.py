import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# --- Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
gc = gspread.authorize(creds)

sheet = gc.open("2025 Draft Tool v1").worksheet("ADP")  # or "Dashboard" depending on where you write

#Grabbing my picks
sheet_2 = gc.open("2025 Draft Tool v1").worksheet("Dashboardv2")  # or "Dashboard" depending on where you write
my_picks = sheet_2.col_values(14)[2:17]  # assuming column B has pick numbers, skip header
my_picks = [int(x) for x in my_picks if x.isdigit()]


# --- Selenium set up
URL_draft = "https://fantasy.espn.com/football/"
options = Options()
options.page_load_strategy = 'none'
#options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get(URL_draft)
time.sleep(2)


# --- Selenium helper ---
def get_drafted_data(driver):
    """Return list of (player_name, team) tuples"""
    try:
        players_picked = driver.find_elements(By.TAG_NAME, "ul")[2]
        player_blocks = players_picked.find_elements(By.TAG_NAME, "li")
    except:
        return []

    drafted_data = []
    for block in player_blocks:
        try:
            text = block.text
            player_name = text.split(" /")[0]
            player_team = text.split(" / ")[1].split(" ")[0]
            player_pos = text.split(" / ")[1].split(" ")[1].split("\n")[0]
            drafted_team = text.split(" / ")[1].split(", ")[1].split("- ")[1]
            drafted_data.append((player_name, player_team, player_pos,drafted_team))
        except:
            continue
    return drafted_data

# --- Main loop ---
input = input("Ready to draft - press enter!")
seen = set()  # track picks we've already processed
current_pick = 1
while True:
    drafted_data = get_drafted_data(driver)
    
    for player, team, pos, d_team in drafted_data:
        if (player, team) not in seen:
            seen.add((player, team))
            print(f"NEW PICK: {player} -> {team}")
            """
            #Currently not working
            row_index = None  # make sure variable always exists
            if current_pick in my_picks:
                pick_col = sheet_2.col_values(14)  # column B holds pick numbers
                try:
                    row_index = pick_col.index(str(current_pick)) + 1  # gspread is 1-based
                except ValueError:
                    row_index = None
            if row_index:
                # Example scraped data from Selenium
                drafted_player = player
                drafted_pos = pos

                # Update player + position into cols O & P
                sheet_2.update_cell(row_index, 15, drafted_player)  # Col O = 15
                sheet_2.update_cell(row_index, 16, drafted_pos)     # Col P = 16
            """



            current_pick += 1
            
            # --- Update your Google Sheet ---
            try:
                cell = sheet.find(player)
                sheet.update_cell(cell.row, 6, True)  # Drafted column is F (6)
                # Update current pick counter in I1
                sheet.update_acell("I1", current_pick)
            except gspread.CellNotFound:
                print(f"{player} not found in sheet!")

    time.sleep(5)  # check every 5 seconds
