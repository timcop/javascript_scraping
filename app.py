from bs4 import BeautifulSoup
import requests

 # try:
    #     element = WebDriverWait(driver, 10).until(
    #         EC.visibility_of_element_located((By.CSS_SELECTOR, '.tm-marketplace-search-card__detail-section.tm-marketplace-search-card__detail-section--link'))
    #     )
    #     print(element)
    # finally:
    #     driver.quit()


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def bsScrape():
    response = requests.get("https://www.bidbud.co.nz/search?page=&category=0002-0356-0032-2273-")
    html = response.content
    # print(response.content)
    soup = BeautifulSoup(html, "html.parser")
    ads = soup.find_all('a', class_="listing_title")
    return ads



def getAdLinks() -> list:
    driver = webdriver.Chrome()
    driver.get("https://www.trademe.co.nz/a/marketplace/computers/laptops/laptops/apple/search?search_string=macbook%20pro")

    href_elements = driver.find_elements(By.CSS_SELECTOR, '.tm-marketplace-search-card__detail-section.tm-marketplace-search-card__detail-section--link')
    hrefs = []
    for e in href_elements:
        hrefs.append(e.get_attribute('href'))

    # Store hrefs as we want to be able to show good deals/link the data back
    
    # Now we want to click through all the search cards and get all info on the individual listings

    return hrefs

# links = getAdLinks()

# response = requests.get(links[0])
# html = response.content
# soup = BeautifulSoup(html, "html.parser")
# ads = soup.find_all('tg-col')

ads = bsScrape()
print(ads[0])