import json

def track_prices():
    data = json.load('./data.json')
    # dumps_json(data)

def main():
    track_prices()

main()
