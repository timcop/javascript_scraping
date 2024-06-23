from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml
import cchardet

from multiprocessing import Pool  # This is a thread-based Pool
from multiprocessing import cpu_count





def getUrls():

    ads_all = []
    base_url = "https://www.bidbud.co.nz/search?category=0002-0356-0032-2273-&page="

    page_num = 1
    max_page_num = 10^10
    response = requests.get("https://www.bidbud.co.nz/search?category=0002-0356-0032-2273-&page=" + str(page_num))
    html = response.content
    soup = BeautifulSoup(html, "lxml")
    page_ads = soup.find_all('a', class_="listing_title")

    ads_all.extend(page_ads)

    print("here1")
    while len(page_ads) > 0:
        print(page_num)
        page_num += 1
        response = requests.get("https://www.bidbud.co.nz/search?category=0002-0356-0032-2273-&page=" + str(page_num))
        html = response.content
        soup = BeautifulSoup(html, "lxml")
        page_ads = soup.find_all('a', class_="listing_title")

        ads_all.extend(page_ads)

    ads_hrefs = [a.get('href') for a in ads_all]

    return ads_hrefs

def scrapeFromUrl(ad):
    
    print("ad: " + ad)
    listing_base_url = "https://www.bidbud.co.nz/"

    response = requests.get("https://www.bidbud.co.nz/" + ad)
    html = response.content
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h2')

    item_info = soup.find('div', id="item_info") # Listing start/end, prices, watches

    description = soup.find('div', id='description') # Description element

    try:
        listing_attributes = description.find('table', id='listingattributes') # table with memory, HDD, screen, cores. Child of description
        attr_rows = listing_attributes.findAll('tr')
        attr_headers = []
        attr_values = []
        for row in attr_rows:
            header = row.find('th').text.strip()
            value = row.find('td').text.strip().strip(':')
            attr_headers.append(header)
            attr_values.append(value)

        # print("here")
        description_paragraphs = description.findAll('p')
        description_paragraphs = [p.text for p in description_paragraphs]
        seller_information = description.find('div', class_='panel-body')
        try:
            member_latest_listings_href = seller_information.find('a', title="View member's listings").get('href')
            member_username = seller_information.find('a', title="View member's listings").text
        except:
            member_latest_listings_href = None
            member_username = seller_information.find('b', class_="warning").text
            print("Warning user")


        member_feedback_href = seller_information.find('a', title="View member's feedback").get('href')
        member_feedback_score = seller_information.find('a', title="View member's feedback").text

        seller_information_string = seller_information.text.strip() # Will need to clean this 
        view_count = soup.find('span', id="view_count").text
        listing_dict = dict()

        # print("here")
        listing_dict['ListingId'] = ad.strip('/')
        listing_dict['Title'] = title.text

        # print("here")
        attrs_dict = dict(zip(attr_headers, attr_values))
        listing_dict.update(attrs_dict)

        listing_dict['Description'] = description_paragraphs

        listing_dict['MemberFeedbackUrl'] = member_feedback_href
        listing_dict['MemberFeedbackScore'] = member_feedback_score
        listing_dict['SellerInformationString'] = seller_information_string

        listing_dict['ViewCount'] = view_count

        listing_dict['ItemInfo'] = item_info.text.strip()

    except:
        listing_dict = dict()


    return listing_dict

def writeDictToCsv(dictionary, path):
    df = pd.DataFrame.from_dict(dictionary)
    df.to_csv(path)


if __name__ == "__main__":

    print("Getting urls....")
    urls = getUrls()
    pool = Pool(cpu_count() * 2)  # Creates a Pool with cpu_count * 2 threads.
    print("Scraping listings...")

    results = pool.map(scrapeFromUrl, urls)  # results is a list of all the placeHolder lists returned from each call to crawlToCSV

    print("Writing to csv...")
    writeDictToCsv(results, 'apple_laptops_bidbud2.csv')

