# Fantasy Football Draft Assistant (Google Sheets + Python)

A live draft assistant that integrates ESPN draft picks and ADP data into a Google Sheets tool.  
Helps fantasy players track live draft results, compare ADP vs PPG value, and rank players by tier.

---

## Features

- **Live ADP Scraping:** Pulls player ADP data from ESPN and updates your Google Sheets draft tool.
- **Real-Time Draft Tracking:** Connects to ESPN draft room via Selenium to update picks dynamically.
- **Tier & Value Analysis:** Calculates ADP vs PPG differences and identifies top-tier players.
- **Interactive Google Sheets Tool:** Dashboard updates automatically based on live picks.

---

## Demo

![Draft Tool Screenshot](assets/draft_tool.gif)  


---

## Getting Started

### Prerequisites

- Python 3.12+
- Google Cloud Service Account with Sheets API enabled
- Required Python packages - see requirements.txt
- Create a file named "service_account.json" wth your Google credentials.

## Updating ADP

- Run **scrape_adp.py** to update the ESPN PPR ADP.  This will push to the ADP Google sheet and flow through to the entire Google Sheet.

## Pre-Draft Use

- The 'Top My Guys Remaining' table on the main dashboard is controlled by the 'My Guys' sheet.  This sheet is a place for you to put players that you are actively targeting in your draft.
  These players are also highlighted green in the other tables on the dashboard.
- You can update the individual position tiers by changing the value in the 'Tier' column inside the QB/RB/WR/TE Tier sheets.  These will then flow into the 'Top Players by Tier' tables on the dashboard.
- You can explore the 'ADP 2024 PPG Value', '2024 Fantasy Finish v ADP', and 'ADP Draft Prep' sheets to explore different value metrics for players based on their 2024 fantasy data.

## Draft Time
- Make sure to type in your correct first pick into P1 in order for the tool to update all of your picks!
  
### Not using the live draft scraper
- This tool can be used as is with no connectivty to the ESPN live draft.  You can use column E to manually mark when players have been drafted to have them excluded from the tables and automatically tick up the 'Current Pick'.
- You can also forego this and manually change the 'Current Pick' in cell S1 after each of your picks in order to update the 'Top Players by Tier' tables.  This will keep them looking at the next 4 picks.

### Using the live draft scraper
- Run the **scrape_live_draft.py** file.
- When the browser opens:
  -   Log in
  -   Navigate to your draft room
  -   When it is time to draft, enter the room
- When the draft room is open and the UI has loaded, press enter in the command prompt to activate the scraper
- As picks are made the draft tool will:
  - Update the current pick
  - Remove players from your draft boards
- You will still want to manually enter your draft picks into the 'My Team' table.  Automation for this to be released in a future version.

Have fun!


