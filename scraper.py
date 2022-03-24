from bs4 import BeautifulSoup
import requests
import time

PREFIX = "https://www.bazaraki.com"

GEARBOX = "1"       # 1 - automatic. 2 - manual. 3 - all.
YEAR_MIN = 2006     # to get amount in link, need to subtract 1949
PRICE_MAX = 6000    # in euros
DELAY = 5           # delay between requests to limit server load

# fixed parts for link to 1st page of the request
LINK_FIRST_PART = "https://www.bazaraki.com/car-motorbikes-boats-and-parts/cars-trucks-and-vans/gearbox---"
LINK_SECOND_PART = "/year_min---"
LINK_THIRD_PART = "/lefkosia-district-nicosia/?price_max="
LINK_WITH_PAGE_THIRD = "/lefkosia-district-nicosia/?page="
LINK_WITH_PAGE_FOURTH = "&price_max="

# request and beautiful soup
response = requests.get(url=f"{LINK_FIRST_PART}{GEARBOX}"
                            f"{LINK_SECOND_PART}{YEAR_MIN - 1949}"
                            f"{LINK_THIRD_PART}{PRICE_MAX}")
start_webpage = response.text
soup = BeautifulSoup(start_webpage, "html.parser")

# get number of last page
last_page = int(soup.select(".number-list a")[-1].text)

# lists for all data
data = []

for n in range(1, last_page + 1):

    # update link and soup if not 1st page
    if n > 1:
        response = requests.get(url=f"{LINK_FIRST_PART}{GEARBOX}"
                                    f"{LINK_SECOND_PART}{YEAR_MIN - 1949}"
                                    f"{LINK_WITH_PAGE_THIRD}{n}"
                                    f"{LINK_WITH_PAGE_FOURTH}{PRICE_MAX}")
        start_webpage = response.text
        soup = BeautifulSoup(start_webpage, "html.parser")

    containers = soup.find_all(class_="announcement-container")
    for container in containers:

        # get images
        try:
            image = container.find(name="img")["src"]
        except TypeError:
            image = ""

        # get titles
        try:
            title = container.find(class_="announcement-block__title").text.replace("\n              ", "")\
                .replace("\n                ", "").replace("\n            ", "").replace("\n          ", "").strip()
        except TypeError:
            title = ""

        # get links
        try:
            link = f"{PREFIX}{container.find(name='a', class_='announcement-block__title')['href']}"
        except TypeError:
            link = ""

        # get descriptions
        try:
            description = container.find(name="div", class_="announcement-block__description").text\
                .replace("\n              ", "").replace("\n                ", "").strip()
        except TypeError:
            description = ""

        # get addresses and publishing dates
        try:
            address = container.find_next(name="div", class_="announcement-block__date").text\
                .replace("\n                  ", "").replace("\n                ", "").replace("\n              ", "")\
                .replace("\n            ", "").replace("\n          ", "").strip()
        except TypeError:
            address = ""

        # get prices
        try:
            price = "€" + container.find_next(name="div", class_="announcement-block__price").text.replace("\n", "")\
                .replace(" ", "").split("€")[1]
        except TypeError:
            price = ""

        # put data into list of dictionaries
        data.append({"image": image,
                     "title": title,
                     "link": link,
                     "description": description,
                     "address": address,
                     "price": price
                     })

    print("Please wait. Loading Data.")

    # delay the next iteration so the server is not under heavy load
    time.sleep(5)
