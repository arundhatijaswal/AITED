from bs4 import BeautifulSoup
import requests
# import sys

# googleURL = "http://www.google.com/"
# searchQuery = "top+10+issues+in+"
# topic = sys.argv[1]
# searchURL = googleURL + searchQuery + topic

# payload = {'key1': 'value1', 'key2': 'value2'}
# r = requests.get("http://httpbin.org/get", params=payload)

# r = requests.post(searchURL)

r = requests.get("http://docs.python-requests.org/en/latest/index.html")
data = r.text
soup = BeautifulSoup(data)

print(soup.get_text())