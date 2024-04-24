import time
from selenium import webdriver
from selenium.common import ElementClickInterceptedException, NoSuchWindowException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def openInNewTab(url):
    driver.execute_script("window.open('" + url + "', '_blank');")


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
                       for product in driver.find_elements(By.CSS_SELECTOR, "article.elDjrO")[:numbersOfProducts]]
        for productUrl in productUrls:
            driver.get(productUrl)

        # close and go to next tab
        driver.close()
    except NoSuchWindowException:
        # If the window is already closed, break the loop
        break

# close
driver.quit()
