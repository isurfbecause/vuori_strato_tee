from core import get_shirts, price_change, send_mail
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
TESTING = os.getenv('TESTING')


def lambda_handler(event, context):
    shirts = get_shirts()

    if TESTING:
        send_mail(shirts)

    if price_change(shirts):
        send_mail(shirts)
        return {
            'statusCode': 200,
            'body': 'Price changed. Email sent.'
        }
    else:
        return {
            'statusCode': 200,
            'body': 'No price change detected.'
        }
