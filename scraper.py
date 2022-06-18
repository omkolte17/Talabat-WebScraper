from bs4 import BeautifulSoup
from time import time
import pandas as pd
import requests
import json

# Function to clean the item description
def cleaner(var):
    return var.replace("\n", "").replace("\r", "").replace("\t", "").strip()

class scraper:
    def scrape(self, url):
        # Parse the page with BeautifulSoup
        r = requests.get(url).content
        soup = BeautifulSoup(r, "html.parser")

        # Initialize the required variables
        sourceData = None
        restaurant_name = None
        restaurant_logo = None
        restaurant_latitude = None
        restaurant_longitude = None
        cuisine_tags = None
        menu_items = []

        # Scraping required data
        try:
            scriptTag = soup.find("script", attrs = {"type":"application/json"}, id = "__NEXT_DATA__")
            sourceData = json.loads(str(scriptTag.string))
        except Exception as e:
            print("Oops! Something Went Wrong!")
    
        # Extract Restaurant Data
        try:
            restaurant_data = sourceData["props"]["pageProps"]["gtmEventData"]["restaurant"]
            menuData = sourceData["props"]["pageProps"]["initialMenuState"]["menuData"]

            restaurant_name = cleaner(restaurant_data["name"])
            cuisine_tags = [restaurant_data["cuisineString"].split(", ")]
            restaurant_logo = restaurant_data["logo"]
            restaurant_latitude = float(restaurant_data["latitude"])
            restaurant_longitude = float(restaurant_data["longitude"])

            # Extract Menu Items
            for items in menuData["items"]:
                menu_items.append([cleaner(items["name"]), cleaner(items["description"]), float(items["price"]), items["originalImage"]])
            
            # Processing done -> return
            return [restaurant_name, restaurant_logo, restaurant_latitude, restaurant_longitude, cuisine_tags, menu_items]
        
        except Exception as e:
            print("Error: ", e)
    

# # # Driver Code
if __name__ == '__main__':
    # Total Time -> 12.5 sec
    start = time()

    # Creating object of class for accessing the driver() method
    scrap = scraper()

    # Get URLs from json file
    with open("data/sample.json", 'r') as file:
        url_data = json.load(file)
    
    fetchedData = []

    for link in url_data:
        print("Scraping From -> ", link)
        fetchedData.append(scrap.scrape(link))
    
    # Create a DataFrame
    df = pd.DataFrame(fetchedData, columns = ["restaurant_name", "restaurant_logo", "latitude", "longitude", "cuisine_tags", "menu_items"])

    # Write data to csv
    df.to_csv("output/data.csv")
    
    end = time()
    print("\nTime Required: ", (end - start))