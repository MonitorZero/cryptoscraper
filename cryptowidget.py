# @author MonitorZero
# Simple scraper for the current prices of ADA, DOGE, and BTC

import requests
from bs4 import BeautifulSoup as bs
import PySimpleGUI as sg
import csv

# The theme for the GUI
sg.theme('Dark Black ')

# Setting up the GUI
layout = [[sg.Text('Total Invested:', font=('Helvetica', 25)), sg.Text('$', font=('Helvetica', 25), key='-grandtotal-')],

           # The names of the cryptocurrencies 
          [sg.Text('ADA:', size=(4, 1), font=(15)), sg.Text('',size=(7,1),font=(15),key='-adaOwned-'),
           sg.Text('DOGE:', size=(6, 1),font=(15)), sg.Text('',size=(8,1),font=(15),key='-dogOwned-'), 
           sg.Text('BTC:', size=(4, 1), font=(15)), sg.Text('',size=(8,1),font=(15),key='-btcOwned-')],

           # The prices of the cryptocurrencies
          [sg.Text('      $ ', size=(0, 0),font=(15)),sg.Text('',font=(15),size=(10,1),key='-ada-'), 
           sg.Text('  $', size=(0, 0),font=(15)),sg.Text('',font=(15),size=(8,1), key='-dog-'),  
           sg.Text('       $', size=(0, 0),font=(15)), sg.Text('',font=(15),size=(10,1),key='-btc-' )],

           # The totals for the cryptocurrencies
            [sg.Text('Total:', size=(0, 0),font=(15)), sg.Text('',font=(15), size=(8,1), key='-adatotal-'),
             sg.Text('Total:', size=(0, 0),font=(15)), sg.Text('',font=(15), size=(8,1), key='-dogtotal-'),
             sg.Text('Total:', size=(0, 0),font=(15)), sg.Text('',font=(15), size=(8,1), key='-btctotal-')],

           # The buttons
          [sg.Button('Refresh'),sg.Button('Edit'), sg.Button('Exit')]]

# Window GUI setup
window = sg.Window('Crypto Price Widget', layout, grab_anywhere=True, no_titlebar=True, keep_on_top=False)

# Function to check if there is a crypto.csv file. If not, create one with 0,0,0 and save it
def check_csv():
    try:
        read_crypto()
    except FileNotFoundError:
        with open('crypto.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['0', '0', '0'])

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

    sg.theme('Dark Blue')

    layout = [
    [sg.Text('Edit your owned cryptocurrencies')],
    [sg.Text('ADA', size=(5,1)), sg.Input(f'{crypto_list[0][0]}', size=(10,1), key='-adaOwn-')],
    [sg.Text('DOGE', size=(5,1)), sg.Input(f'{crypto_list[0][1]}', size=(10,1), key='-dogOwn-')],
    [sg.Text('BTC', size=(5,1)), sg.Input(f'{crypto_list[0][2]}', size=(10,1), key='-btcOwn-')],
    [sg.Text("")],
    [sg.Button('Save'), sg.Button('Cancel')]
    ]

    win = sg.Window('Edit your owned cryptocurrencies', layout, keep_on_top=True, modal=True, no_titlebar=True, grab_anywhere=True)

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
        check_csv()
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
        window['-adatotal-'].update(f'{float(ownedCrypto[0][0]) * ada_price:.2f}')
        window['-dogtotal-'].update(f'{float(ownedCrypto[0][1]) * doge_price:.2f}')
        window['-btctotal-'].update(f'{float(ownedCrypto[0][2]) * btc_price:.2f}')
        # Update the grandtotal key and format for currency display
        window['-grandtotal-'].update(f'$ {float(ownedCrypto[0][0]) * ada_price + float(ownedCrypto[0][1]) * doge_price + float(ownedCrypto[0][2]) * btc_price:,.2f}')
    if event == 'Edit':
        check_csv()
        edit_crypto()