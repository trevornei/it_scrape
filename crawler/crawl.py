import requests
import bs4

url = "https://www.umt.edu/it"

response = requests.get(url)

soup = bs4.BeautifulSoup(response.content, "html.parser")

main = soup.find("main")

anchor = main.find_all('a')
for a in anchor:
    print(a.text)