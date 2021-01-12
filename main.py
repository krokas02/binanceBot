from binance.client import Client
from time import sleep
import os
import configparser
import json


def clear(): os.system('cls')  # On Windows


# def clear(): os.system('clear')  # On Linux

inputFile = open('currencies.json')
jsonArray = json.load(inputFile)
currencies = jsonArray['currencies']

config = configparser.ConfigParser()
config.read("settings.ini")
api = config['API']
apiKey = api['api_key']
apiSecret = api['api_secret']

client = Client(apiKey, apiSecret)

values = config['VALUES']
quantity = values['buy_value']
buyPercent = values['buy_percent']
order = False

mainLoop = True
print("##########################################")
print("########### Python Binance Bot ###########")
print("##########################################")
while mainLoop:
    print("Input: ")
    inputCommand = input()
    clear()
    if inputCommand == "end":
        mainLoop = False
    elif inputCommand == "api":
        print("Api key: ")
        apiKey = input()
        print("Api secret: ")
        apiSecret = input()
        client = Client(apiKey, apiSecret)
        clear()
        config.set("API", "api_key", apiKey)
        config.set("API", "api_secret", apiSecret)
    elif inputCommand == "start":
        while not order:
            for x in currencies:
                symbol = x
                print(symbol)
                BTC = client.get_historical_klines(symbol=symbol, interval='3m', start_str="1 hour ago UTC")
                if ((float(BTC[-1][2]) - float(BTC[-2][3])) / float(BTC[-2][3]) * 100) > float(buyPercent):
                    print('Buyyy')
                    client.order_market_buy(symbol=symbol, quantity=quantity)
                    order = True
                else:
                    print('Do nothing')
                sleep(0.2)

    with open("settings.ini", 'w') as configfile:
        config.write(configfile)
