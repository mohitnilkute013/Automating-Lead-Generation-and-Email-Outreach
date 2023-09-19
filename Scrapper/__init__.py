from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import re
from logger import logger

class Scrapper:

    def __init__(self):
        # Initialize a headless Chrome browser
        self.driver = webdriver.Chrome()


    def open_url(self, url):
        """Opens up an url in chrome."""
        try:
            # Navigate to the webpage
            self.driver.get(url)
            time.sleep(2)
            logger.info(f"Opened {url}.")
        except Exception as e:
            logger.error(f"Failed to open URL: {url}.")

    def search_place(self, place_name:str, searchBoxId:str, submitButtonXPath:str):
        '''
        Searches for places using Google Maps API in search box and opens the searched location website.
        '''
        try:
            logger.info(f"Searching for {place_name}.")
            searchBox = self.driver.find_element(By.ID, searchBoxId)
            searchBox.clear()

            searchBox.send_keys(place_name)

            submit = self.driver.find_element("xpath", submitButtonXPath)
            submit.click()
            time.sleep(5)
        except Exception as e:
            logger.error(f"Error in Searching {place_name}.")

    def getXPathElement(self, xpath):
        return self.driver.find_element("xpath", xpath)#[0]

    
    def getByCssSelector(self, selector, element_type):

        '''
        Returns element from CSS Selector if found else returns None
        '''
        element = None

        try:
            element = self.driver.find_element("css selector", selector).text
            logger.info(f"Found '{element_type}': '{element}'")
        except Exception as e:
            logger.error(f"Element of type '{element_type}' not found.")
            # pass

        return "NA" if element is None else element


    def getByClassName(self, class_name, element_type):
        '''
        Returns element by Class Name if found else returns None
        '''
        element = None

        try:
            element = self.driver.find_element(By.CLASS_NAME, class_name).text
            logger.info(f"Found '{element_type}': '{element}'")
        except Exception as e:
            logger.error(f"Element of type '{element_type}' not found.")
            # pass

        return "NA" if element is None else element 

    def __del__(self):
        # Closing the browser when done
        self.driver.quit()
        logger.info("Browser Closed.")

if __name__ == '__main__':

    csv_file_path = "leads.csv"

    scraper=Scrapper()
    scraper.open_url("https://www.google.com/maps")

    search = input("Enter search industry and location: ")

    # Store the data in a CSV file
    with open(csv_file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        # Write header row
        writer.writerow(["Name", "Address", "Website", "Phone Number", "Rating", "Email ID"])

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
            
            # Write lead data
            writer.writerow([Name, location, website, ph_no, rating, Email])

    logger.info(f"Scrapped data written into {csv_file_path}")

    del scraper