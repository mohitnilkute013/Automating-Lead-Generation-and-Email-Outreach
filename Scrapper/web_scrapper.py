import csv
import requests
from bs4 import BeautifulSoup as bs

query = "Google Pune"

# Define the URL for Google Maps with your search query
url = f"https://www.google.com/maps/search/{query}"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    soup = bs(response.text, "html.parser")

    # Extract business information (replace with actual HTML tags)
    business_name = soup.find("div", class_="AeaXub").text.strip()
    # business_address = soup.find("div", class_="business-address").text.strip()
    
    # Store the data in a CSV file
    with open("leads.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        # Write header row
        writer.writerow(["Name", "Address"])
        # Write lead data
        writer.writerow([business_name, "business_address"])
else:
    print("Failed to retrieve data from Google Maps.")
