import gspread
from google.oauth2.service_account import Credentials

def get_worksheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file("service.json", scopes=scopes)
    client = gspread.authorize(creds)

    sheet = client.open("FIXTURES")
    worksheet = sheet.worksheet("seed")

    return worksheet
