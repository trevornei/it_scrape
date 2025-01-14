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
        if not any(d['Parent URL: '] == url for d in dont_replicate):
            dont_replicate.append({
                "Parent URL: ": url
            })
            # print(dont_replicate)
        else:
            print(f"\033[31mThis url was a duplicate ---x \033[0m {url}")
            continue

anti_replicator()
print(f"\n\033[92mThis is new the culled list:\033[0m \033[94m{len(dont_replicate)}\033[0m {dont_replicate}")




""" Now Iterate over the cleaned list of URL's. """

def crawl_child_elements(depth=0, max_depth=20):
    # iterate through the elements in cleaned list. 
    for p in dont_replicate:
        sidebar_elements = soup.find_all('div', class_='sidebar-template')
        for element in sidebar_elements:
            c_href = element.find_all('a', href=True)
            for link in c_href:
                child_href_value = link.get('href', '')
                if any(d['Parent URL: '] == child_href_value for d in dont_replicate):
                    print(f"\033[31mThis child url is a duplicate ---x \033[0m {child_href_value}")
                else:
                    print(f"\033[92mThis child url is unique:\033[0m {child_href_value}")
                    child_elements = {f"Child URL {len(dont_replicate) + 1}": child_href_value}
                    dont_replicate.append({
                        "Parent URL: ": child_href_value,
                        "Child Elements": child_elements
                    })

crawl_child_elements()

def save_to_file(filename):
    with open(filename, 'w') as file:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file.write(f"# Saved on: {timestamp}\n")
            file.write(f"dont_replictate = {dont_replicate}")

# Example usage
save_to_file('cleaned_urls.txt')

print(dont_replicate)