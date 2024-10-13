from core import get_shirts, price_change, send_mail


def lambda_handler(event, context):
    shirts = get_shirts()
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
