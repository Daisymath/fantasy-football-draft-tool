#Scrape the ADP from ESPN and update the Google Sheet

#Import Libraries
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Target URL
URL_adp = "https://fantasy.espn.com/football/livedraftresults"

#Set up options
options = Options()
options.page_load_strategy = 'none'
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get(URL_adp)
time.sleep(4)

#Scrape ADP
pages = [0,1,2,3]
adp = []
for i in pages:
    print("Running "+str(i))
    rows = driver.find_elements(By.TAG_NAME,"tr")
    for j in range(2,52):
        temp = rows[j].text
        #The injury tag changes the format of the text in the tag
        if temp.split('\n')[2] in ['Q','SSPD','O']:
            temp_data = temp.split('\n')[:2]
            temp_data.extend(temp.split('\n')[3:6])
        else:
            temp_data = temp.split('\n')[:5]
        adp.append(temp_data)
    #find and define the 'next' button
    path = "//button[@data-nav-item='"+str(i+2)+"']"
    buttons = driver.find_elements(By.XPATH,path )
    #press the button to go to the next page
    buttons[0].click()
    #wait for loading
    time.sleep(5)

driver.close()

#Create data frame and transform to match sheet
df_adp = pd.DataFrame(adp,columns=['Rank','Player','Team','Pos','ADP'])
df_adp = df_adp[~df_adp['Pos'].isin(['K','D/ST'])]
#Travis Hunter!
df_adp['Pos'] = df_adp['Pos'].str[:2]
# Clean Rank and ADP columns
df_adp["Rank"] = df_adp["Rank"].str.replace("'", "", regex=False).astype(float)
df_adp["ADP"] = df_adp["ADP"].str.replace("'", "", regex=False).astype(float)
#Reorder to match form of GSheet
new_order = ['Rank','Player','ADP','Pos']
df_adp_upload = df_adp.copy()
df_adp_upload = df_adp_upload[new_order]
df_adp_upload = df_adp_upload.rename({'Player':'Name'},axis=1)

#Save
df_adp_upload.to_csv('adp_scrape_update.csv',index=False)


#Upload to GSheet
# -------------------------------
# Google Sheets Setup
# -------------------------------
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

# Open your sheet
sheet = client.open("2025 Draft Tool v1").worksheet("ADP_Stg0")  # ADP sheet with Drafted column

# Convert DataFrame into list of lists (with header row first)
adp_data = [df_adp_upload.columns.tolist()] + df_adp_upload.astype(str).values.tolist()

# Dynamically set the range width based on df shape
num_rows = len(adp_data)
num_cols = df_adp_upload.shape[1]
last_col_letter = chr(64 + num_cols)

sheet.update(f"A1:{last_col_letter}{num_rows}", adp_data)