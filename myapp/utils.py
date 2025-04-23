import requests

def fetch_sheet_data(sheet_id, range_name, api_key):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/1J2P_DDmpbrkTQzgykXXlr4e9winAk7yMqu7z70KFchU/values/Data!A1:Z100?key=AIzaSyDR4jGJHp7kaHFyOJfy99hKV3UXLHvyu-c"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
