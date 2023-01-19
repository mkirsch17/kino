import os
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver


def retrieve_highlights():
    """Retrieve highlights for all books via Amazon Cloud Reader"""

    all_highlights = []

    driver = webdriver.Firefox()
    driver.get("https://read.amazon.com/notebook")

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
        book.click()
        driver.implicitly_wait(2)
        highlights_elements = driver.find_elements(By.ID, "highlight")
        highlights = []
        for highlight_element in highlights_elements:
            highlights.append(highlight_element.text)

        book_info = {"title": title, "author": author, "highlights": highlights}
        all_highlights.append(book_info)

    return all_highlights


if __name__ == "__main__":

    highlights = retrieve_highlights()

    with open("highlights.json", "w") as outfile:
        json.dump(highlights, outfile)
