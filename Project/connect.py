from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import pandas as pd



# Load credentials from the JSON file
credentials = Credentials.from_service_account_file('credentials.json')
# Create the service client
service = build('sheets', 'v4', credentials=credentials)


#FEATURE IMPORTANCE 
featureImp = pd.read_csv(r'featureImp.csv')
header = featureImp.columns.tolist()
data = [header] + featureImp.values.tolist()

spreadsheet_id = '1j7BlrO0pzhJEYWfvAHAB5ksydNg2n-Ad3woYjD9EcEo'  # Replace with your spreadsheet ID
range_name = 'Sheet1!A1'  # Replace with the range where you want to write the data

body = {
    'values': data
}

try:
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='RAW', body=body
    ).execute()
    print(f"{result.get('updatedCells')} cells updated.")

except HttpError as error:
    print(f"An error occurred: {error}")
    print(f"Response status: {error.resp.status}")
    print(f"Response content: {error.content}")


#Loss data for Scatter Plot
lossMetrics = pd.read_csv(r'LossMetrics.csv')
header2 = lossMetrics.columns.tolist()
data2 = [header2] + lossMetrics.values.tolist()

spreadsheet_id2 = '1hBnsTSdiRdFRDa5JC0EIwkFb7fuKxZDN0188sWU1RvQ'  # Replace with your spreadsheet ID
range_name2 = 'Sheet1!A1'

body2 = {
    'values': data2
}

try:
    result2 = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id2, range=range_name2,
        valueInputOption='RAW', body=body2
    ).execute()
    print(f"{result2.get('updatedCells')} cells updated.")

except HttpError as error:
    print(f"An error occurred: {error}")
    print(f"Response status: {error.resp.status}")
    print(f"Response content: {error.content}")


#PERFORMANCE METRICS
with open('best_metrics.json', 'r') as file:
     best_metrics = json.load(file)
     best_metrics = pd.DataFrame(best_metrics, index=[0])
     header3 = best_metrics.columns.tolist()
     data3 = [header3] + best_metrics.values.tolist()

spreadsheet_id3 = '1FuQ_DATFKatketfduRcsvDYPByOMb7jklVExEmEAcCo'  # Replace with your spreadsheet ID
range_name3 = 'Sheet1!A1'

body3 = {
    'values': data3
}

try:
    result3 = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id3, range=range_name3,
        valueInputOption='RAW', body=body3
    ).execute()
    print(f"{result3.get('updatedCells')} cells updated.")

except HttpError as error:
    print(f"An error occurred: {error}")
    print(f"Response status: {error.resp.status}")
    print(f"Response content: {error.content}")