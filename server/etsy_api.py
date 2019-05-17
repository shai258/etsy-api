import requests
import random
from flask import Flask, render_template

app = Flask(__name__)

key = 'hwxuyigooh52kkgwjc95yi6p'
shops_param = 'wildlifegardenerart,blondevagabond,sunnyprint'
fields = 'shop_name'
includes = 'Listings(title,price):active:50/Images(url_75x75):1'

api_url = f'https://openapi.etsy.com/v2/shops/{shops_param}?fields={fields}&includes={includes}&api_key={key}'
headers = {'Content-Type': 'application/json'}


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/shops")
def get_shops_info():
    response = requests.get(api_url, headers)

    if response.status_code == 200:
        shops = response.json()['results']
        parsed_response = []
        for shop in shops:
            parsed_shop = {'shop_name': shop['shop_name'], 'listings': []}
            # Get a random sample of 3 unique listings:
            listings = random.sample(shop['Listings'], 3)

            for listing in listings:
                parsed_shop['listings'].append(
                    {'title': listing['title'],
                     'price': listing['price'],
                     'img_url': listing['Images'][0]['url_75x75']})

            parsed_response.append(parsed_shop)
        return render_template('shops.html', shops=parsed_response)
    else:
        return False


if __name__ == '__main__':
    app.run(debug=True)
