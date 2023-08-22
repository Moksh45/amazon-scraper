import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# Function to extract additional product details from a product URL
def extract_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract product details
    product_description_tag = soup.find("meta", attrs={"name": "description"})
    product_description = product_description_tag["content"] if product_description_tag else "N/A"

    asin_tag = soup.find("th", string="ASIN")
    asin = asin_tag.find_next_sibling("td").string.strip() if asin_tag else "N/A"

    manufacturer_tag = soup.find("th", string="Manufacturer")
    manufacturer = manufacturer_tag.find_next_sibling("td").string.strip() if manufacturer_tag else "N/A"

    return product_description, asin, manufacturer



# URL of the Amazon search results page
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"

# Number of pages to scrape
num_pages = 20

# Initialize a list to store data
data = []

# Loop through each page
for page in range(1, num_pages + 1):
    url = base_url + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract product data
    products = soup.find_all("div", {"data-asin": True})
    
    for product in products:
        product_link = product.find("a", {"class": "a-link-normal"})
        if product_link:
            product_link = product.find("a", {"class": "a-link-normal"})
            if product_link:
                product_url = "https://www.amazon.in" + product_link["href"]
        # Extract product name
            product_name_elem = product.find("span", {"class": "a-text-normal"})
            product_name = product_name_elem.text.strip() if product_name_elem else "N/A"
        # product_names.append(product_name)
        
        # Extract product price
            product_price_elem = product.find("span", {"class": "a-offscreen"})
            product_price = product_price_elem.text.strip() if product_price_elem else "N/A"
            # product_prices.append(product_price)
        
        # Extract product rating
            rating_elem = product.find("span", {"class": "a-icon-alt"})
            rating = rating_elem.text.split()[0] if rating_elem else "N/A"
            # ratings.append(rating)
        
        # Extract number of reviews
            num_review_elem = product.find("span", {"class": "a-size-base"})
            num_review = num_review_elem.text.split()[0] if num_review_elem else "0"
            # num_reviews.append(num_review)
            
            # Extract additional product details
            product_description, asin, manufacturer = extract_product_details(product_url)
            
            # Append data to the list
            data.append([
                product_name, product_price, rating, num_review, product_url,
                product_description, asin, manufacturer
            ])

# Create a DataFrame from the collected data
columns = ["Product Name", "Product Price", "Rating", "Number of Reviews", "Product URL",
           "Product Description", "ASIN", "Manufacturer"]
df = pd.DataFrame(data, columns=columns)

# Export the DataFrame to a CSV file
df.to_csv("amazon_product_data.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)
