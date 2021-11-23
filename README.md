# cryptoscraper
Crypto Widget for ADA, DOG, and BTC

Uses PySimpleGUI to build a simple widget that can sit on your desktop

By default it will scrape coinmarketcap whenever you press the "Refresh" button on the widget.

Right now only supports the hardcoded coins ADA, DOGE, and BTC.

You can edit your owned quantity of the coins by hitting "Edit" and putting in the appopriate quantities.

Your quantity owned is stored in a csv file named crypto.csv.

Then you'll be sent back to the widget, hit "Refresh", and you'll see your owned amount, current amount of owned, and total investment on the top.

Total investment is approximate due to the .2f formatting of the currencies.



All source code can be found in the cryptowidget.py file and you're free to modify the widget to your liking.

I tried to make most things very straight forward in the comments so it should be as easy as copy and pasting some elements.
