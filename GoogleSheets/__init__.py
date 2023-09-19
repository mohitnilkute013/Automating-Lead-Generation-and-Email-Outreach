import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
import pandas as pd
from logger import logger

class GoogleSheetsManager:

    def __init__(self, credential_json, spreadsheet_name:str = None):

        # Define the scope and credentials file
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(credential_json, scope)

        try:
            # Authenticate with Google Sheets API
            self.client = gspread.authorize(creds)
        except Exception as e:
            logger.error("Not able to authorize Google Sheets. Make sure the Google Sheets API and Google Drive API is Enabled on 'website': 'https://console.cloud.google.com/projectselector2/apis/dashboard?pli=1&supportedpurview=project&authuser=1'")

        if spreadsheet_name is not None:
            self.open_spreadsheet(spreadsheet_name)

    
    def open_spreadsheet(self, spreadsheet_name:str):

        '''
        Opens a spreadsheet, if not exists then creates a new one.

        Params:
        spreadsheet_name: name of the spreadsheet to be opened or created.

        Returns:
        spreadsheet: spreadsheet object refering to the new spreadsheet.
        '''
        
        try:
            # Try to open the existing Google Sheet by name
            spreadsheet = self.client.open(spreadsheet_name)

        except gspread.exceptions.SpreadsheetNotFound:
            # If the spreadsheet doesn't exist, create a new one
            spreadsheet = self.client.create(spreadsheet_name)

        return spreadsheet


    def open_worksheet(self, spreadsheet_name, worksheet_name):

        '''
        Opens a worksheet, if not exists then creates a new one.

        Params:
        worksheet_name: name of the worksheet to be selected or created.

        Returns:
        worksheet: worksheet object refering to the new worksheet.
        '''

        try:
            # Try to open the existing worksheet by title
            worksheet = self.client.open(spreadsheet_name).worksheet(worksheet_name)

        except gspread.exceptions.WorksheetNotFound:
            # If the worksheet doesn't exist, create a new one
            worksheet = self.client.open(spreadsheet_name).add_worksheet(worksheet_name, 1, 1)

        return worksheet


    def store_from_csv(self, worksheet, csv_file):
        '''
        Stores data from CSV file into specified worksheet
        '''
        try:
            # Read the scraped data from the CSV file
            with open(csv_file, mode="r") as file:
                reader = csv.reader(file)
                # next(reader)  # Skip the header row
                for row in reader:
                    # Append the data to the Google Sheets document
                    worksheet.append_row(row)
                    
            logger.info("Completed Storing of csv file data to Google Sheets.")
        except Exception as e:
            print("Exception in storing csv file in google sheets.")
            logger.info("Error in Storing data from csv file to specified worksheet in Google Sheets.")


    def store_data(self, worksheet, data):

        if isinstance(data, pd.DataFrame):
            # If data is a DataFrame, convert it to a list of lists
            data = data.values.tolist()

        elif isinstance(data, str):
            # If data is a string, assume it's a CSV file path and read data from the CSV file
            data_from_csv = pd.read_csv(data)
            data = data_from_csv.values.tolist()
            
        elif isinstance(data, list):
            # If data is already a list, leave it as is
            pass

        else:
            raise ValueError("Unsupported data type. Please provide data as a DataFrame, a list, or a CSV file path.")

        if data:
            print(data)
            # Append the data to the worksheet
            # worksheet.append_rows(data)
            for row in data:
                print("wrtten", row)
                # Replace "NA" with None
                cleaned_data = [None if item == "NA" else item for item in row]
                # Append the data to the Google Sheets document
                worksheet.append_row(cleaned_data)



if __name__ == '__main__':

    gsm = GoogleSheetsManager(credential_json="credentials\email-generation-using-chatgpt-9e8df841d5ff.json")

    spreadsheet = gsm.open_spreadsheet(spreadsheet_name="Email Generation using Chatgpt")

    worksheet = gsm.open_worksheet(spreadsheet_name="Email Generation using Chatgpt", worksheet_name="Sheet1")

    gsm.store_from_csv(worksheet=worksheet, csv_file="leads.csv")