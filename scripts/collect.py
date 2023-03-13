import os
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import logging


def retrieve_highlights():
    """Retrieve highlights for all books via Amazon Cloud Reader"""

    logging.info("Retrieving highlights...")
    all_highlights = []

    driver = webdriver.Firefox()
    actions = ActionChains(driver)
    driver.get("https://read.amazon.com/notebook")

    logging.info("Logging into Amazon Notebook...")
    username_textbox = driver.find_element(By.ID, "ap_email")
    username_textbox.send_keys(os.environ["KINDLE_USERNAME"])
    password_textbox = driver.find_element(By.ID, "ap_password")
    password_textbox.send_keys(os.environ["KINDLE_PASSWORD"])
    signin_button = driver.find_element(By.ID, "signInSubmit")
    signin_button.submit()

    driver.implicitly_wait(2) # seconds
    books = driver.find_elements(By.CLASS_NAME, "kp-notebook-library-each-book")
    sleep(5)

    for book in books:
        title, author = book.text.split("\n")
        logging.info(f"Parsing highlights for title: {title}...")
        book.click()
        driver.implicitly_wait(2)
        last_accessed_element = driver.find_element(By.ID, "kp-notebook-annotated-date")
        last_accessed_text = " ".join(last_accessed_element.text.split()[1:])   # Drop day of week
        last_accessed = datetime.strptime(last_accessed_text, "%B %d, %Y")
        last_accessed_str = datetime.strftime(last_accessed, "%d_%m_%y")

        highlights_elements = driver.find_elements(By.ID, "highlight")
        highlights_count = len(highlights_elements)

        more_highlights = True
        while more_highlights:
            sleep(1) # Not sure why this is needed, but it is
            driver.execute_script("arguments[0].scrollIntoView();", highlights_elements[-1])
            highlights_elements = driver.find_elements(By.ID, "highlight")

            if highlights_count == len(highlights_elements):
                more_highlights = False
            else:
                highlights_count = len(highlights_elements)

        highlights = []
        for highlight_element in highlights_elements:
            highlights.append(highlight_element.text)

        book_info = {"title": title, "author": author, "last_accessed": last_accessed_str, "highlights": highlights}
        all_highlights.append(book_info)

    return all_highlights
