from bs4 import BeautifulSoup
import requests

r = requests.get("http://www.pythonforbeginners.com/python-on-the-web/web-scraping-with-beautifulsoup/")
data = r.text
soup = BeautifulSoup(data)

print(soup.get_text())