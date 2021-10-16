# BeerWulf 
# Render Dynamic Pages 
# Tutorial from John Watson Rooney YouTube channel

from requests_html import HTMLSession
import pandas as pd

session = HTMLSession()

drinklist = []

def request(url):
    url = 'https://www.beerwulf.com/en-gb/c/all-beers'
    r = session.get(url)
    # Loads browser in the background and renders the page
    r.html.render(sleep=1)
    status = r.status_code
    return r.html.xpath('//*[@id="product-items-container"]', first=True)

def parse(products):
    for item in products.absolute_links:
        r = session.get(item)
        name = r.html.find('div.product-detail-info-title', first=True).text
        info = r.html.find('div.product-subtext', first=True).text
        price = r.html.find('span.price', first=True).text

        try:
            rating = r.html.find('span.label-stars', first=True).text
        except: 
            rating = 'No rating'
        
        # If the div 'add-to-cart-container' is present, then there is stock available. 
        if r.html.find('div.add-to-cart-container'):
            stock = 'In stock'
        else:
            stock = 'Out of stock'

        drink = {
            'name': name, 
            'info': info, 
            'price': price, 
            'rating': rating, 
            'stock': stock,
        }

        drinklist.append(drink)

def output():
    df = pd.DataFrame(drinklist)
    df.to_csv('BeefWulf.csv')
    print('Saved items to CSV file.')

x = 1
while True:
    try: 
        products = request(f'https://www.beerwulf.com/en-gb/c/all-beers?catalogCode=Beer_1&routeQuery=all-beers&page={x}')
        print(f'Getting items from page {x}')
        parse(products)
        print('Total items: ', len(drinklist))
        x += 1

    except:     
        print('No more pages.')
        
output()