import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from get_crypto import pricemonitor

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SAMPLE_SPREADSHEET_ID = '1c5Lw1a1nNmIhVkodrV87Q7BWLKgV4vwsZqoZpzviv-w'

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        # Call the Sheets API
        sheet = service.spreadsheets()

        coin_data = pricemonitor()
        row = 2
        for data in coin_data:
            service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"Sheet1!A{row}",
                valueInputOption="USER_ENTERED", body={"values": [[f'{data["name"]}']]}).execute()
            service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"Sheet1!B{row}",
                valueInputOption="USER_ENTERED", body={"values": [[f'{data["symbol"]}']]}).execute()
            service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"Sheet1!C{row}",
                valueInputOption="USER_ENTERED", body={"values": [[f"₹{data['market_cap']}"]]}).execute()
            service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"Sheet1!D{row}",
                valueInputOption="USER_ENTERED", body={"values": [[f"₹{data['price']}"]]}).execute()
            service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"Sheet1!E{row}",
                valueInputOption="USER_ENTERED", body={"values": [[f"{data['percent_change_1h']}%"]]}).execute()
            row += 1
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()