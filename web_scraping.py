import time
from selenium import webdriver
from selenium.common import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

driver = webdriver.Chrome()
driver.get('https://digitec.ch/de')

try:
    # Wait for the search input to be clickable
    search_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "q"))
    )
    # Perform the search
    search_input.click()
    search_input.send_keys("S24")
    search_input.send_keys(Keys.ENTER)

    # Clicking the first article
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='productListingContainer']/div[4]/article[1]"))
    ).click()
    print(f"Navigate to article")

    # Get brand name
    product_brand_name = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='pageContent']/div/div[1]/div[1]/div/div[2]/div/div[1]/div/h1/strong"))
    ).text
    print(f"Product Brand Name: {product_brand_name}")

    # Get product name
    product_name = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='pageContent']/div/div[1]/div[1]/div/div[2]/div/div[1]/div/h1/span"))
    ).text
    print(f"Product Name: {product_name}")

    # Get description
    product_description = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='pageContent']/div/div[1]/div[1]/div/div[2]/div/div[1]/div/span"))
    ).text
    print(f"Product Description: {product_description}")

    # Get price
    product_price = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='pageContent']/div/div[1]/div[1]/div/div[2]/div/div[1]/span/strong/button/span"))
    ).text
    print(f"Product Price: {product_price}")

    # Get overall rating
    product_rating = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='pageContent']/div/div[1]/div[1]/div/div[2]/div/div[2]/div[1]/a/span[3]"))
    ).get_attribute("aria-label")
    print(f"Product Rating: {product_rating}")

    # Go to all reviews page
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.LINK_TEXT, "Zu weiteren Produktbewertungen"))
    ).click()

    # Get all reviews
    reviews = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='pageContent']/div/ul/li"))
    )
    if reviews:
        print(f"Number of Reviews: {len(reviews)}")
    else:
        print("No reviews found.")

    all_reviews = []

    for index, review in enumerate(reviews, start=1):
        # Initialize an empty dictionary to store the review details
        review_details = {}

        # Get review rating
        review_rating = review.find_element(By.XPATH, ".//article/div[1]/span").get_attribute("aria-label")
        review_details["rating"] = review_rating

        # Get review title
        review_title = review.find_element(By.XPATH, ".//h4").text
        review_details["title"] = review_title

        # Get review description
        review_description_elements = review.find_elements(By.XPATH, ".//article/div[1]/p")
        review_description = review_description_elements[0].text if review_description_elements else None
        review_details["description"] = review_description

        # Get review pros
        review_pros_elements = review.find_elements(By.XPATH,".//article/div[1]/div[2]/div/ul[1]/li")
        review_pros = [element.text for element in review_pros_elements]
        review_details["pros"] = review_pros

        # Get review cons
        review_cons_elements = review.find_elements(By.XPATH,".//article/div[1]/div[2]/div/ul[2]")
        review_cons = [element.text for element in review_cons_elements]
        review_details["cons"] = review_cons

        # Append the review details to the list of all reviews
        all_reviews.append(review_details)

    # Write the data to a JSON file
    with open('reviews.json', 'w') as f:
        json.dump(all_reviews, f, indent=4)
    # input("Press any key to continue...")

except TimeoutException:
    print("Timeout while waiting for reviews to load.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
