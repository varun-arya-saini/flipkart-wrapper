import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

item = "laptop"   
url = f"https://www.flipkart.com/search?q={item}"
res = requests.get(url=url)
web_page = res.text
soup = BeautifulSoup(web_page,features="lxml")
item_heading = (soup.title.string)
main_div = soup.find_all("div", {"class": "DOjaWF gdgoEp"})
data_set = []
if len(main_div):
    for sub_div in main_div:
        _div = sub_div.find_all("div", {"class": "cPHDOP col-12-12"})
        if len(_div):
            for item in _div:
                item_set = {}
                item_content = item.find_all("div",{"class":"KzDlHZ"})
                item_content_2 = item.find_all("div",{"class":"hCKiGj"})
                item_content_3 = item.find_all("div",{"class":"slAVV4"})
                if len(item_content):
                    item_price = item.find_all("div",{"class":"Nx9bqj _4b5DiR"})
                    item_content_2 = item.find_all("a",{"class":"WKTcLC BwBZTg"})
                    item_details = item.find_all("li",{"class":"J+igdf"})
                    review = item.find_all("span",{"class":"Wphh3N"})
                    if len(review):
                        review = review[0].find_all("span")
                    r = ""
                    if len(item_content):
                        item_name = item_content[0].get_text()
                        itm_prc = item_price[0].get_text()
                        item_set["item_name"] = item_name
                        if len(review):
                            r = review[0].get_text()
                        item_set["review"] = r
                        item_set["item_price"] = itm_prc
                        it_dt = []
                        for it_detail in item_details:
                            it_dt.append(it_detail.get_text())
                        item_set["item_detail"] = it_dt
                    if item_set:
                        data_set.append(item_set)
                elif item_content_2:
                    for item in item_content_2:
                        item_set = {}
                        item_set["brand_name"] = item.find("div",{"class":"syl9yP"}).get_text()
                        item_set["item_name"] = item.find("a",{"class":"WKTcLC"}).get_text()
                        item_set["item_price"] = item.find("div",{"class":"hl05eU"}).get_text()  
                        if item_set:
                         print(item)
                         data_set.append(item_set)
                elif item_content_3:
                    for item in item_content_3:                       
                        item_set["brand_name"] = item.find("a",{"class":"wjcEIp"}).get_text()
                        item_set["item_price"] = item.find("div",{"class":"hl05eU"}).get_text()
                        if item_set:                         
                         data_set.append(item_set)

print(data_set)
fields = ['item_name', 'review', 'item_price', 'item_detail']
filename = f"{item_heading}.csv"
with open(filename, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)    
    writer.writeheader()
    writer.writerows(data_set)