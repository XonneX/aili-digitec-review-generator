import time
from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

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

    print()
    print(" ########################################## ")
    print()

    for index, review in enumerate(reviews, start=1):

        # Scroll the review into view
        driver.execute_script("arguments[0].scrollIntoView(true);", review)
        time.sleep(1)  # Add a short delay to ensure the element is fully in view

        # Check if there is a "more" button and click it
        more_button_elements = review.find_elements(By.XPATH, ".//div[1]/p/button")
        if more_button_elements:
            try:
                more_button_elements[0].click()
            except ElementClickInterceptedException:
                print("Element click intercepted, trying alternative method...")
                # If click is intercepted, try clicking via JavaScript
                driver.execute_script("arguments[0].click();", more_button_elements[0])

        # Get review title
        review_title = review.find_element(By.XPATH, ".//h4").text

        # Get review rating
        review_rating = review.find_element(By.XPATH, ".//article/div[1]/span").get_attribute("aria-label")

        # Get review description
        review_description_elements = review.find_elements(By.XPATH, ".//article/div[1]/p")
        review_description = review_description_elements[0].text if review_description_elements else None

        # Get review pros
        review_pros = review.find_elements(By.XPATH,".//article/div[1]/div[2]/div/ul[1]")
        review_pros = [element.text for element in review_pros]

        # Get review cons
        review_cons = review.find_elements(By.XPATH,".//article/div[1]/div[2]/div/ul[2]")
        review_cons = [element.text for element in review_cons]

        print(f"Review Index: {index}")
        print(f"Review rating: {review_rating}:")
        print(f"Review Title: {review_title}")
        print(f"Review Description: {review_description}")
        print(f"Review Pros: {review_pros}")
        print(f"Review Cons: {review_cons}")

        print()
        print(" ########################################## ")
        print()


    #input("Press any key to continue...")


except Exception as e:
    print(e)
finally:
    driver.quit()