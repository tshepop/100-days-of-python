import requests
from bs4 import BeautifulSoup
from smtplib import SMTP
import config

FROM_EMAIL = "test.pyCoding@gmail.com"
PASS_FROM = config.EMAIL_PASS
TO_EMAIL = "testpycod3@yahoo.com"
MESSAGE = ", that's wonderful it is below $100 now!."

url = "https://www.amazon.com/Philips-Kitchen-Appliances-Technology-HD9270/dp/B08SHR1QFS/ref=sr_1_1?keywords=air+fryer&qid=1706391845&refinements=p_89%3APHILIPS&rnid=2528832011&s=home-garden&sr=1-1"

head = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}

req = requests.get(url=url, headers=head)
#print(req.status_code)
html_page = req.text
#print(html_page)

soup = BeautifulSoup(html_page, "lxml")
#print(soup.prettify())
price_tag = soup.find("span", class_="a-price-whole")
product_title = soup.find("span", id="productTitle")
#print(tag)
#print(product_title)

price = price_tag.get_text()
title = product_title.get_text().strip()

rice = float(price)
print("Product Title:", title)
print("Price:", price)

buy_price = 100
if price < buy_price:
    with SMTP("smtp.gmail.com", port=587) as server:
        server.starttls()
        server.login(user=FROM_EMAIL, password=PASS_FROM)
        server.sendmail(from_addr=FROM_EMAIL,to_addrs=TO_EMAIL, msg=f"Subject: Amazon price drop\n\n{product_title} {MESSAGE}")
else:
    print(f"The price has not dropped below ${buy_price}")
