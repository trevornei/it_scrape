import requests
import bs4
from urllib.parse import urljoin
import anytree
from anytree import AnyNode, node,RenderTree
from datetime import datetime
home_url = "https://www.umt.edu/it/"

response = requests.get(home_url)

soup = bs4.BeautifulSoup(response.content, "html.parser")

main = soup.find("main")

# URL's List
https_urls = []

# For loop iterates over the main content of the website. 

def scrape_home ():
    for element in main:
        if element == soup.find("div", class_="sidebar-template"):
            href = element.find_all("a", href=True)
            count = 0

            # for loop iterates each discovered href.
            # --> not every href is complete with https
            # ----> Rather, some href's are just slugs.
            for link in href:
                count += 1
                # Handles for the href's that only have slugs.
                # Uses the urljoin library to add home_url to slugs.
                href_value = link.get('href', '')
                if not href_value.startswith("https"):
                    inspire_https = urljoin(home_url, href_value) 
                    https_urls.append(inspire_https)
                    # print(f"The value of the new url join is: {inspire_https} \n The count is: {count} \n \n")

                if href_value.startswith("https"):
                    https_urls.append(href_value) 


scrape_home()
print("\n")
print("\n")
print(f"List of URL's with HTTPS  --> \n \n {https_urls} \n \nThe length of the https_urls dictionary is: {len(https_urls)} \nBREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK  \n \n \n")

dont_replicate = []

# Removes repetitive items in the list of urls.
def anti_replicator ():
    for url in https_urls:
        if url not in dont_replicate:
            dont_replicate.append(url)
            # print(dont_replicate)
        else:
            print(f"This url was a dublicate ---x {url}")
            continue


anti_replicator()
print(len(dont_replicate))