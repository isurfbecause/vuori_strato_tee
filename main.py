import requests
import json
import os
import base64
import requests
from dotenv import load_dotenv
from mailgun import Mailgun

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
EMAIL_DOMAIN = os.getenv('EMAIL_DOMAIN')
MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL')
TO_EMAIL = os.getenv('TO_EMAIL').split(',')

DESIRED_SIZE = 'm'
SHIRT = 'strato-tech-tee-white'

results = []

def send_mail(content):
    print(content)

    print({
        'EMAIL_DOMAIN': EMAIL_DOMAIN,
        'MAILGUN_API_KEY': MAILGUN_API_KEY,
        'FROM_EMAIL': FROM_EMAIL,
        'TO_EMAIL': TO_EMAIL
    })

    try:
        # Create the message data
        message_data = {
            'from': FROM_EMAIL,
            'to': TO_EMAIL,
            'subject': 'Vuori Scraper',
            'text': json.dumps(content,  separators=(',', ':')),
        }

        response = requests.post(
            f"https://api.mailgun.net/v3/{EMAIL_DOMAIN}/messages",
            auth=('api', MAILGUN_API_KEY),
            data=message_data
        )

        # Check response
        if response.status_code == 200:
            print('Email sent successfully:', response.json())
        else:
            print('Failed to send email:', response.status_code, response.text)

    except Exception as error:
        print('Error sending email:', error)


def get_shirts():
    url = 'https://vuoriclothing.com/_next/data/GZ0DfYXEaTrNQt0GABivj/en-US/products/' + SHIRT + '.json'

    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()  # Parse JSON response
        # Dump JSON response as a string for output
        json_string = json.dumps(json_data['pageProps'], indent=2)
        json_string = json.dumps(json_data['pageProps']['pdpPageProps']['variants'], indent=2)

        for v in json_data['pageProps']['pdpPageProps']['variants']:
            options = v['selectedOptions']
            size = options[1]['value']
            is_desired_size = size.lower() == DESIRED_SIZE
            color = options[0]['value']
            color = options[0]['value']
            price = v['price']
            in_stock = v['availableForSale']

            if (is_desired_size and in_stock):
                d = {'color': color, 'size': size, 'price':price}
                results.append(d)

        sorted_results = sorted(results, key=lambda x: x['price'])
        print(sorted_results)
        return sorted_results
    else:
        print(f"Failed to retrieve: {url}")

def price_change(shirts):
    PRICE_CHANGED = False

    price_diff = shirts[0].get('price')
    print('price_diff:' + str(price_diff))

    for shirt in shirts[1:]:
        shirt_price = shirt.get('price')

        if shirt_price != price_diff:
            price_diff = shirt_price
            PRICE_CHANGED = True

    if PRICE_CHANGED:
        print('send email')
    else:
        print('No price change. Email will not be sent.')

    return PRICE_CHANGED

shirts = get_shirts()

if price_change(shirts):
    send_mail(shirts)
