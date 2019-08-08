from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1bo34Knob4ihKBY6eWFhxpUTkyHXYzylv8yiMZvhFq5M'  # noqa '1OJsQqaJBOmaoC1-SCuXX110ae5wb8AWbKFzG_PgzMUM'
RANGE = 'A1:ZZ'


# Code from https://developers.google.com/sheets/api/quickstart/python
def createService():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    return service


def readSheet(sheetName):
    service = createService()
    sheetRange = sheetName + '!' + RANGE

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=sheetRange).execute()
    values = result.get('values', [])

    return values


def writeSheet(sheetName, values):
    service = createService()
    sheet = service.spreadsheets()
    sheetRange = sheetName + '!' + RANGE
    sheetBody = {'values': values}

    result = sheet.values.update(spreadsheetId=SPREADSHEET_ID,
                                 range=sheetRange,
                                 valueInputOption='USER_ENTERED',
                                 body=sheetBody).execute()

    return result


# def main():
#     service = createService()

#     # Call the Sheets API
#     sheet = service.spreadsheets()
#     result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
#                                 range=SAMPLE_RANGE_NAME).execute()


#     values = result.get('values', [])

#     print(values)
#     values.append(['testing adding'])

#     testBody = {'values': values}

#     result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
#                                    range=SAMPLE_RANGE_NAME,
#                                    valueInputOption='USER_ENTERED',
#                                    body=testBody).execute()

# def findMethods(obj):
#     method_list = [func for func in dir(obj) if callable(getattr(obj, func))]
#     return method_list
