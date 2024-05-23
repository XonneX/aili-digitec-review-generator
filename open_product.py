import time
from selenium import webdriver
from selenium.common import ElementClickInterceptedException, NoSuchWindowException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json


def openInNewTab(url):
    driver.execute_script("window.open('" + url + "', '_blank');")


def scan_product():
    # Get brand name
    try:
        product_brand_name = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='pageContent']/div/div[1]/div[1]/div/div[2]/div/div[1]/div/h1/strong"))
        ).text
        print(f"Product Brand Name: {product_brand_name}")

        # Get product name
        product_name = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='pageContent']/div/div[1]/div[1]/div/div[2]/div/div[1]/div/h1/span"))
        ).text
        print(f"Product Name: {product_name}")

        # Get description
        product_description = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div/div[1]/div[2]/div/div/main/div/div[1]/section[1]/div[1]/div/div/div/div/div/span/span"))
        ).text
        print(f"Product Description: {product_description}")

        # Get price
        product_price = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='pageContent']/div/div[1]/div[1]/div/div[2]/div/div[1]/span/strong/button"))
        ).text
        print(f"Product Price: {product_price}")

        # Get overall rating
        product_rating = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='pageContent']/div/div[1]/div[1]/div/div[2]/div/div[2]/div[1]/a/span[3]"))
        ).get_attribute("aria-label")
        print(f"Product Rating: {product_rating}")
        
        # Get basic product info
        product_info = {
            "brand_name": product_brand_name,
            "name": product_name,
            "description": product_description,
            "price": product_price,
            "rating": product_rating
        }

        # Go to all reviews page
        review_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".hPsIoK"))
        )
        driver.get(review_button.get_attribute("href"))
    
        # Get all reviews
        reviews = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "[data-cy='review']"))
        )
        if reviews:
            print(f"Number of Reviews: {len(reviews)}")
        else:
            print("No reviews found.")
    
        product_reviews = []
    
        for index, review in enumerate(reviews, start=1):
            # Initialize an empty dictionary to store the review details
            review_details = {}
    
            # Get review rating
            review_rating = review.find_element(By.CSS_SELECTOR, ".star_stars__LYfBH")
            review_details["rating"] = review_rating.get_attribute("aria-label")
    
            # Get review title
            review_title = review.find_element(By.XPATH, ".//h4").text
            review_details["title"] = review_title
    
            # Get review description
            review_description_elements = review.find_elements(By.CSS_SELECTOR, ".klxbRk")
            review_description = review_description_elements[0].text if review_description_elements else None
            review_details["description"] = review_description
    
            # Get review pros
            review_details["pros"] = []
            try:
                review_pros_anchor = review.find_elements(By.CSS_SELECTOR, ".cNqvxA")[0]
                if review_pros_anchor:
                    review_pros_elements = review_pros_anchor.find_elements(By.CSS_SELECTOR, "span")
                    review_pros = [element.text for element in review_pros_elements]
                    review_details["pros"] = review_pros
            except IndexError:
                print("No pros found")
    
            # Get review cons
            review_details["cons"] = []
            try: 
                review_cons_anchor = review.find_elements(By.CSS_SELECTOR, ".cNqvxA")[1]
                if review_cons_anchor:
                    review_cons_elements = review_cons_anchor.find_elements(By.CSS_SELECTOR, "span")
                    review_cons = [element.text for element in review_cons_elements]
                    review_details["cons"] = review_cons
            except IndexError:
                print("No cons found")
    
            # Append the review details to the list of all reviews
            product_reviews.append(review_details)
    
        # Create a dictionary to store both the product info and the reviews
        data = {
            "product_info": product_info,
            "reviews": product_reviews
        }
        return data
    except:
        return None


# config values
categoriesCSS = ".gQqszz"
numbersOfProducts = 9

driver = webdriver.Chrome()
driver.get('https://digitec.ch/de')

# get all categories from the left side
categoriesUl = (WebDriverWait(driver, 10)
                .until(EC.visibility_of_element_located((By.CSS_SELECTOR, categoriesCSS))))
categories = categoriesUl.find_elements(By.CSS_SELECTOR, "li a")

# print names
# skip last to because sales and second hand are not product categories
for item in categories[:-2]:
    category_url = item.get_attribute("href")
    openInNewTab(category_url)

products = []
# process category
while len(driver.window_handles) > 1:
    try:
        # switch to new tab
        driver.switch_to.window(driver.window_handles[-1])
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "body")))

        # print category name
        category_name = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h1"))).text
        print(f"Category: {category_name}")

        # get n products
        productUrls = [product.find_element(By.TAG_NAME, "a").get_attribute("href")
                       for product in driver.find_elements(By.CSS_SELECTOR, "article.fOimcc")[:numbersOfProducts]]
        for productUrl in productUrls:
            driver.get(productUrl)
            product_data = scan_product()
            products.append(product_data)

        # close and go to next tab
        driver.close()
    except NoSuchWindowException:
        # If the window is already closed, break the loop
        break

# Write the data to a JSON file
with open('reviews.json', 'w') as f:
    json.dump(products, f, indent=4)
# close
driver.quit()
