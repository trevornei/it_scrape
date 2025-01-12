import requests
import bs4
from urllib.parse import urljoin

home_url = "https://www.umt.edu/it"

response = requests.get(home_url)

soup = bs4.BeautifulSoup(response.content, "html.parser")

main = soup.find("main")

# URL's List
https_urls = [] 

# For loop iterates over the main content of the website. 

for element in main:
    if element == soup.find("div", class_="sidebar-template"):
        href = element.find_all("a", href=True)

        # for loop iterates each discovered href.
        # --> not every href is complete with https
        # ----> Rather, some href's are just slugs.
        for link in href:
            # Handles for the href's that only have slugs.
            # Uses the urljoin library to add home_url to slugs.
            href_value = link.get('href', '')
            if not href_value.startswith("https"):
                inspire_https = urljoin(home_url, href_value) 
                https_urls.append(inspire_https)

            if href_value.startswith("https"):
               https_urls.append(href_value) 
    

print("\n")
print("\n")
print(f"List of URL's with HTTPS  --> \n \n {https_urls}")
