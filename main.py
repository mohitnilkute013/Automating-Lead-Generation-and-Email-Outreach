import os
import csv
import time
import pandas as pd
from dotenv import load_dotenv

from Scrapper import Scrapper
from selenium.webdriver.common.by import By
from GoogleSheets import GoogleSheetsManager
from SendEmail import EmailSender

import openai
from logger import logger

csv_file_path = input("Enter CSV File Path: ")

load_dotenv("credentials\.env")  # Load variables from .env file

# Set your OpenAI API key and other credentials
openai.api_key = os.environ.get('OPENAI_API_KEY')
email_address = os.environ.get('EMAIL')
email_password = os.environ.get('PASSWORD')


scraper=Scrapper()
scraper.open_url("https://www.google.com/maps")

search = input("Enter search industry and location: ")

# Scrape the data from Google maps and Store the data in a CSV file
logger.info(f"Scrapping from Google Maps and Writing to {csv_file_path} file.")

df = pd.DataFrame({'Name':[],
        'Address':[],
        'Website':[],
        'Phone Number':[],
        'Rating':[],
        'Email ID':[]
       })

scraper.search_place(search, "searchboxinput", "/html/body/div[3]/div[8]/div[3]/div[1]/div[1]/div/div[2]/div[1]/button")

companies = scraper.driver.find_elements(By.CLASS_NAME, "hfpxzc")

for company in companies:
    company.click()
    time.sleep(3)

    Name = scraper.getByClassName(class_name="DUwDvf", element_type="Name")
    print(f"Company Name: {Name}")

    location = scraper.getByCssSelector(selector="[data-item-id='address']", element_type="address")
    print(f"Company Address: {location}")

    website = scraper.getByCssSelector(selector="[data-item-id='authority']", element_type="authority")
    print(f"Website: {website}")

    ph_no = scraper.getByCssSelector(selector="[data-item-id*='phone:tel:']", element_type="phone:tel")
    print(f"Phone Number: {ph_no}")

    rating = scraper.getByClassName(class_name="F7nice ", element_type="rating")
    print(f"Rating: {rating}")

    Email = "mohitnilkute012@gmail.com"

    df2 = pd.DataFrame({'Name':[Name],
        'Address':[location],
        'Website':[website],
        'Phone Number':[ph_no],
        'Rating':[rating],
        'Email ID':[Email]
       })

    df = pd.concat([df, df2], ignore_index = True)
    df.reset_index()

# logger.info(df)

del scraper

# Write the DataFrame to the CSV file
df.to_csv(csv_file_path)
logger.info(f"Scrapped data written into {csv_file_path}")

# Initialize Google Sheet manager for storing data to google sheets
gsm = GoogleSheetsManager(credential_json="credentials\gsheet.json")

# Creating Spreadsheet 
spreadsheet = gsm.open_spreadsheet(spreadsheet_name="Email Generation using Chatgpt")

# Creating Spreadsheet and Worksheet
worksheet = gsm.open_worksheet(spreadsheet_name="Email Generation using Chatgpt", worksheet_name="Sheet1")

# Storing the data to the worksheet
gsm.store_from_csv(worksheet=worksheet, csv_file=csv_file_path)


all_emails = []
status_arr = []

# Create an EmailSender instance
email_sender = EmailSender(email_address, email_password)

# Iterate through the data to generate emails and consequently send emails.
for i in range(df.shape[0]):
    row = df.loc[i]

    # Extract information from the row
    company_name = row['Name']
    address = row['Address']
    website = row["Website"]
    ph_no = row['Phone Number']
    rating = row['Rating']
    email_id = row['Email ID']
    
    # Create a message for the company
    message = f"Write an Email to the CEO of {company_name}, Website: {website}, Company Address {address}, asking for some more information about their business for further business deal."
    try:
        # Generate email content using the OpenAI API
        output = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )
    except Exception as e:
        logger.error("Error with Open AI API, please check your credentials.")
    
    # Extract the generated email text
    email_text = output['choices'][0]['message']['content']
    all_emails.append(email_text)
    logger.info(f"Email to {company_name}: {email_text}")

    status = email_sender.send_email(business_name=company_name, to_email=email_id, subject="Testing", body=email_text)
    # status = True
    status = "Success" if status == True else "Failed"
    status_arr.append(status)
    logger.info(f"Email Sent Status: {status}")

# Close the email server connection
email_sender.close()



# Add the 'Email Text' column to the DataFrame
df["Email Text"] = all_emails
df["Status"] = status

# Write the updated DataFrame to the CSV file
df.to_csv(csv_file_path)
logger.info(f"Updated data written into {csv_file_path}")

# Storing the updated data to Google Sheets
# Convert the DataFrame to a list of lists
updated_data_values = df.values.tolist()

# Update the Google Sheet with the new data, including 'Email Text' column
worksheet.update([df.columns.values.tolist()] + updated_data_values)
logger.info("Updated Google Sheet with Email Text and Status.")