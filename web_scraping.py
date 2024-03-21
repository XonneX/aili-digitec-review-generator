from selenium import webdriver
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
    search_input.send_keys("Iphone")
    search_input.send_keys(Keys.ENTER)

    # Clicking the first article
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='productListingContainer']/div[4]/article[1]"))
    ).click()

    # Get brand name
    product_brand_name = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='pageContent']/div/div[1]/div[1]/div/div[2]/div/div[2]/h1/strong"))
    ).text

    # Get product name
    product_name = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='pageContent']/div/div[1]/div[1]/div/div[2]/div/div[2]/h1/span"))
    ).text

    # Get description
    product_description = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='pageContent']/div/div[1]/div[1]/div/div[2]/div/div[2]/span"))
    ).text

    # Get price
    product_price = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@class='sc-125c42c7-5 hMyxKO']//span"))
    ).text

    # Get overall rating
    product_rating = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'star_stars__LYfBH')]"))
    ).get_attribute("aria-label")

    print(f"Product Brand Name: {product_brand_name}")
    print(f"Product Name: {product_name}")
    print(f"Product Description: {product_description}")
    print(f"Product Price: {product_price}")
    print(f"Product Rating: {product_rating}")

    # Go to all reviews page
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='pageContent']/div/div[1]/section[7]/div[3]/div[3]/div/div[2]/a"))
    ).click()

    # Get all reviews
    reviews = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='pageContent']/div/div[4]/ul/li"))
    )

    for index, review in enumerate(reviews, start=1):

        # Check if there is a "more" button
        #more_button_elements = review.find_elements(By.XPATH, ".//div[1]/p/button")
        #if more_button_elements:
        #    more_button_elements[0].click()

        # Get review title
        review_title = review.find_element(By.XPATH, ".//h4").text

        # Get review rating
        review_rating = review.find_element(By.XPATH, ".//article/div[1]/span").get_attribute("aria-label")

        # Get review description
        review_description_elements = review.find_elements(By.XPATH, ".//article/div[1]/p/span/span")
        review_description = review_description_elements[0].text if review_description_elements else None
        additional_description_elements = review.find_elements(By.XPATH, ".//article/div[1]/p/span[2]/span")
        additional_description = additional_description_elements[0].text if additional_description_elements else None

        # Get review pros
        review_pros = review.find_elements(By.XPATH,
                                           ".//article/div[1]/div[2]/div/ul[1]")
        review_pros = [element.text for element in review_pros]

        # Get review cons
        review_cons = review.find_elements(By.XPATH,
                                           ".//article/div[1]/div[2]/div/ul[2]")
        review_cons = [element.text for element in review_cons]

        print(f"Review Index: {index}")
        print(f"Review rating: {review_rating}:")
        print(f"Review Title: {review_title}")
        print(f"Review Description1: {review_description}")
        print(f"Review Description2: {additional_description}")
        print(f"Review Pros: {review_pros}")
        print(f"Review Cons: {review_cons}")


    #input("Press any key to continue...")


except Exception as e:
    print(e)
finally:
    driver.quit()