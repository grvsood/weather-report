import pandas as pd
from bs4 import BeautifulSoup
import requests as rq
import json
import sys
try:
    from urllib.request  import urlopen
except ImportError:
    from urllib2 import urlopen

#retrives current user location
def location_lookup():
    try:
        return json.load(urlopen('http://ipinfo.io/json'))
    except:
        print("Unable to retreive location from http://ipinfo.io\nTry Again after some time\n")
        sys.exit(1)

#gets current user details
location = location_lookup()

#url for web scrapping
url = "https://weather.com/en-IN/weather/today/l/" + str(location["loc"])

page = rq.get(url)
#print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())

today = soup.find(class_ = "today_nowcard-container")
#print(today.prettify())

loc = [today.select(".today_nowcard-location")[0].get_text()]
asof = [list(today.select(".today_nowcard-timestamp")[0].children)[1].get_text()]
temp = [today.select(".today_nowcard-temp")[0].get_text() + "C"]
short_desc = [today.select(".today_nowcard-phrase")[0].get_text()]
feels_like = [today.select(".deg-feels")[0].get_text()]

#Obtain Weather Conditions Report
right_now = today.select(".today_nowcard-sidecar")[0].find_all("tr")
desc = {}
desc_list = ["Wind", "Humidity", "Dew Point", "Pressure", "Visibility"]
cols = []
for row in right_now:
    cols.append(row.find_all('td')[0].text.strip())

for i in range(len(desc_list)):
    desc[desc_list[i]] = cols[i]

#Full Weather Desccription
details = soup.find(class_ = "dp-details").find(class_ = "today-wx-descrip").get_text()


weather = pd.DataFrame({
    "Location": loc,
    "As of": asof,
    "Temp": temp,
    "Short Desc": short_desc,
    "Feels Like": feels_like
}, index = ['Details'])


print(weather)
print("")
for key,value in desc.items():
    print(key + " : " + value)
print("Full Description: " + details)
