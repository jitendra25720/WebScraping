from lib2to3.pgen2.grammar import opmap_raw
from turtle import st
from urllib import response
import requests
import pandas as pd
from bs4 import BeautifulSoup
import random
import regex as re

reviewlist = []
# r = requests.get('http://httpbin.org/ip', proxies=proxy, verify=False)
# print(r.text)

def getRandomProxy():
    proxy = {
    "http": f"http://scraperapi:APIKey@proxy-server.scraperapi.com:8001",
    "https": f"http://scraperapi:APIKey@proxy-server.scraperapi.com:8001"}

    return proxy


def extractReviews(reviewUrl, pageNumber):
    resp = requests.get(reviewUrl, proxies=getRandomProxy(), verify=False)
    soup = BeautifulSoup(resp.text, 'html.parser')
    reviews = soup.findAll('div',{'data-hook':'review'})

    print(reviews)

    for item in reviews:
        # with open('output/file_with_2.html', 'w') as f:
        #     f.write(str(item))
        # break
        reviews = {
            'productTitle' : soup.title.text.replace("Amazon.in:Customer reviews: ", "").strip(),
            'Review Title' : item.find('a',{'data-hook':"review-title"}).text.strip(),
            'Rating' : item.find('i',{'class':"review-rating"}).text.strip(),
            'Review Body' : item.find('div',{'class':"a-row a-spacing-small review-data"}).text.strip()
        }
        # break
        reviewlist.append(reviews)
        print(reviews)
    
def totalpages(productUrl):
    resp = requests.get(productUrl, proxies=getRandomProxy(), verify=False)
    soup = BeautifulSoup(resp.text, 'html.parser')
    review = soup.find('div',{'data-hook':'cr-filter-info-review-rating-count'})
    pages = str(review.text.strip().split(', ')[1].split(" ")[0])
    # print(re.sub(',',"",pages))
    return int(re.sub(',',"",pages))

def main():
    productUrl = "https://www.amazon.in/realme-Cancellation-Bluetooth-Headset-Wireless/dp/B08V9XS5M6/ref=sr_1_3"
    reviewUrl = productUrl.replace("dp", "product-reviews") + "?pageNumber=" + str(3)
    # print(reviewUrl)
    totalpg = totalpages(reviewUrl)
    # return totalpg

    for i in range(totalpg//10):
        print(f"Running for page {i}")
        try:
            reviewUrl = productUrl.replace("dp", "product-reviews") + "?pageNumber=" + str(i)
            extractReviews(reviewUrl, i)
        except Exception as e:
            print(e)
    print(reviewlist)
    df = pd.DataFrame(reviewlist)
    df.to_csv('Reviews.csv')

main()

