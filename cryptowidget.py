# @author Andrew Janicke
# Simple scraper for the current prices of ADA, DOGE, and BTC

import requests
from bs4 import BeautifulSoup as bs
import PySimpleGUI as sg
import csv

# The theme for the GUI
sg.theme('Dark Blue 3')

# Setting up the GUI
layout = [[sg.Text('Crypto Price Widget', font=('Helvetica', 25))],

           # The names of the cryptocurrencies 
          [sg.Text('ADA:', size=(4, 1)), sg.Text(f'', size=(7,1), key='-adaOwned-'),
           sg.Text('DOGE:', size=(5, 1)), sg.Text(f'', size=(8,1), key='-dogOwned-'), 
           sg.Text('BTC:', size=(4, 1)), sg.Text(f'', size=(8,1), key='-btcOwned-')],

           # The prices of the cryptocurrencies
          [sg.Text('     $ ', size=(0, 0)),sg.Text('', size=(10,1), key='-ada-'), 
           sg.Text('  $', size=(0, 0)),sg.Text('', size=(7,1), key='-dog-'),  
           sg.Text('       $', size=(0, 0)), sg.Text('', size=(10,1), key='-btc-' )],

           # The totals for the cryptocurrencies
            [sg.Text('Total:', size=(0, 0)), sg.Text('', size=(8,1), key='-adatotal-'),
             sg.Text('Total:', size=(0, 0)), sg.Text('', size=(8,1), key='-dogtotal-'),
             sg.Text('Total:', size=(0, 0)), sg.Text('', size=(8,1), key='-btctotal-')],

           # The buttons
          [sg.Button('Refresh'),sg.Button('Edit'), sg.Button('Exit')]]

# Window GUI setup
window = sg.Window('Crypto Price Widget', layout, grab_anywhere=True, no_titlebar=False, keep_on_top=False)


# Scrape the bitcoin data
def btc_scrape():
    r = requests.get('https://coinmarketcap.com/currencies/bitcoin/')
    soup = bs(r.content, 'html.parser')
    bitcoin_price = soup.find('div', class_='priceValue').get_text()
    bitcoin_price = bitcoin_price.replace(',', '')
    bitcoin_price = bitcoin_price.replace('$', '')
    bitcoin_price = float(bitcoin_price)
    return bitcoin_price

# scrape the dogecoin data
def doge_scrape():
    r = requests.get('https://coinmarketcap.com/currencies/dogecoin/')
    soup = bs(r.content, 'html.parser')
    doge_price = soup.find('div', class_='priceValue').get_text()
    doge_price = doge_price.replace(',', '')
    doge_price = doge_price.replace('$', '')
    doge_price = float(doge_price)
    return doge_price

# Scrape the ada data
def ada_scrape():
    r = requests.get('https://coinmarketcap.com/currencies/cardano/')
    soup = bs(r.content, 'html.parser')
    ada_price = soup.find('div', class_='priceValue').get_text()
    ada_price = ada_price.replace(',', '')
    ada_price = ada_price.replace('$', '')
    ada_price = float(ada_price)
    return ada_price

# Function to edit your owned cryptocurrencies and store them into a csv file
def edit_crypto():
    # Open crypto.csv file and store the data into a list
    with open('crypto.csv', 'r') as f:
        crypto = csv.reader(f, delimiter=',')
        crypto_list = list(crypto)
        print(crypto_list)
        
    layout = [
    [sg.Text('Edit your owned cryptocurrencies')],
    [sg.Text('ADA', size=(5,1)), sg.Input(f'{crypto_list[0][0]}', size=(10,1), key='-adaOwn-')],
    [sg.Text('DOGE', size=(5,1)), sg.Input(f'{crypto_list[0][1]}', size=(10,1), key='-dogOwn-')],
    [sg.Text('BTC', size=(5,1)), sg.Input(f'{crypto_list[0][2]}', size=(10,1), key='-btcOwn-')],
    [sg.Button('Save'), sg.Button('Cancel')]
    ]
    

    win = sg.Window('Edit your owned cryptocurrencies', layout, keep_on_top=True, modal=True)

    event, values = win.read()
    if event == sg.WINDOW_CLOSED or event == 'Cancel' or event == 'Exit0':
        win.close()
    if event == 'Save':
        with open('crypto.csv', 'w') as f:
            csv.writer(f, delimiter=',').writerow([values['-adaOwn-'], values['-dogOwn-'], values['-btcOwn-']])
        win.close()
    window.write_event_value(event, values)

# Function to read the crypto.csv file and store the data into a list
def read_crypto():
    with open('crypto.csv', 'r') as f:
        crypto = csv.reader(f, delimiter=',')
        crypto_list = list(crypto)
        print(crypto_list)
        return crypto_list

# Event code
while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WINDOW_CLOSED or event == 'Exit' or event == 'Exit0':
        break
    if event == 'Refresh':
        ownedCrypto = read_crypto()
        btc_price = btc_scrape()
        doge_price = doge_scrape()
        ada_price = ada_scrape()
        window['-btc-'].update(btc_price)
        window['-dog-'].update(doge_price)
        window['-ada-'].update(ada_price)
        window['-adaOwned-'].update(ownedCrypto[0][0])
        window['-dogOwned-'].update(ownedCrypto[0][1])
        window['-btcOwned-'].update(ownedCrypto[0][2])
        window['-adatotal-'].update(str(float(ownedCrypto[0][0]) * ada_price))
        window['-dogtotal-'].update(str(float(ownedCrypto[0][1]) * doge_price))
        window['-btctotal-'].update(str(float(ownedCrypto[0][2]) * btc_price))
    if event == 'Edit':
        edit_crypto()