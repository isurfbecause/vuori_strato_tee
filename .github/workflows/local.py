from core import get_shirts, price_change, send_mail

shirts = get_shirts()

if price_change(shirts):
    send_mail(shirts)
    print('Price changed. Email sent.')
else:
    print('No price change detected.')
