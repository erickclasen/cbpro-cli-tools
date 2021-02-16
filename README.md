# cbpro-cli-tools

This set of Python files allows operations on Coinbase Pro that can be done from the Web UI to be done
from the command line via Python. Frequently the interface to Coinbase Pro via the API
is more resonsive during time of high load on the Coinbase Pro exchange.
Orders can be set,cancelled or read easier at times from the command line and these tools
provide an easy way to work in a command line mode with Coinbase Pro.

Additionally for the initiated there is enough code base in the files, especially the
coretamodule.py and cbpro_buy_sell.py to "roll your own" automated trading code that could
be called periodically via CRON to manage trading/investing on the Coinbase Pro Exchange by
using raw Python, with the exception of the requirement of installing the cbpro module.

This code was made a straightforward as possible to minimize the amount of libraries needed and
the "heaviness" of overhead so it can be deployed easily and on lightweight hardware such as
a Raspberry Pi.

Note: Access the Coinbase Pro API via cbpro requires Python3 to work with SSL.

## Reminder
Although this code has been used in production successfully, there is no guarantee that it is
bug free and will always remain in working order.
 Always consider the risk when using code that transacts using real money that can be lost.
 No one can be responsible for the operation of the code or finanacial transactions
other than the end user of this code. A person on r/Wallstreetbets said it best when they had
the following comment in their post signature...
"Don't take what I have as financial advice as I am totally high right now." We might not all
be high but we are human and suffer from all kinds of failure modes. The fate of Long Term
Capital Management comes to mind, look it up, it is a worthy tale of a brilliant but epic fail.

## Operations

Operations such as...

- Creating buy and sell orders
- Printing a list of open orders and a summary of the last 5 filled orders
- Cancelling orders
- Reading Accounts * This requires downloading data and keeping it updated for prices/volume. See below


## Requirements
Requires the Python client code for the Coinbase Pro API provided by Daniel Paquin
https://github.com/danpaquin/coinbasepro-python

For reference ...
- https://docs.pro.coinbase.com/

- You may manually install the project or use ```pip```:
```python
pip install cbpro
#or
pip install git+git://github.com/danpaquin/coinbasepro-python.git
```

## Key, Passphrase and b64secret
To use this code you have to modify defines.py to include these credentials obtained from Coinbase Pro and it is best to set 
permissions to r/w for user. As in, chmod 600 it.

## Ticker data
The ticker filename is required for the cbpro_read_accts.py.
The ticker price and volume can be pulled down by calling...

cbpro-api-price-volume-ticker-5-cryptos-csv.py

on an hourly basis to create the ticker csv file.
A seed file to start from is kept updated at...

http://heart-centered-living.org/public/cbpro-data/cbpro_crypto_price_volume_file.csv


defines.py must contain as a minimum the key, b64secret and passphrase for the Coinbase Pro API.
Coinbase provides instructions for this...

https://help.coinbase.com/en/pro/other-topics/api/how-do-i-create-an-api-key-for-coinbase-pro

## Brief explanations of files.
Some of the files produce logs of their actions, such as buying and selling. Look for files
ending in .log in the directory that this code in ran under.
These logs are a good place to find the order id if the status of the order is to be checked in
the future by using...

python3 print-cbpro-orders.py fill order-id-here




## Support files used as modules by the code
 There is quite a bit of extra code in the files which can be used to build automated trading
 code from by using these files as a module above and beyond what they are used for in
 cbpro-cli-tools
coretamodule.py         
cbpro_buy_sell.py

## defines.py - Holds the Keys and Ticker Filename (optional for all buy cbpro_read_accts.py)

## Information

##print-cbpro-orders.py

Takes 2 arguments. action (OPEN/FILL),id (or ALL or RECENT for OPEN or product id/ order id for FILL)

	 EX: python3 print-cbpro-orders.py open all

##cbpro_read_accts.py

Prints the prices and the amounts held in each asset in size and USD.
Also prints out the portfolio total to portfolio_size.json

	EX: python3 cbpro_read_accts.py

## Ticker Data

##cbpro-api-price-volume-ticker-5-cryptos-csv.py

This code gets called periodically via CRON to keep a csv with price/volume data, the ticker file.
This file is used by cbpro_read_accts.py and is optional for the others.
This file outputs the data to a location hardcoded in the file. 
A seed file to get started with historic data is available at http://heart-centered-living.org/public/cbpro-data/cbpro_crypto_price_volume_file.csv

	EX: python3 cbpro-api-price-volume-ticker-5-cryptos-csv.py

## Action 
These pieces of code perform an action and will present the action to be performed and
ask for a confimation before carrying it out.

Glossary:
action = buy or sell.

currency = the currency to buy into or sell from.

underlying = the asset that is to be bought from or sold to, think BTC-USD, USD as the underlying.


##cancel-limit-orders.py
Takes 3 arguments. currency,underlying, and order code or all

	EX: python3 cancel-limit-orders.py btc usd all


##manual-market-order.py
Market orders take 5 arguments. action, $ funds,currency & underlying.

	EX: python3 manual-market-order.py buy 100 btc usd


##manual-limit-orders.py
Limit orders take 6 arguments. action,size,currency,underlying, and price

	EX: python3 manual-limit-orders.py sell 0.001 btc usd 49970

##manual-stop-orders.py
Stop orders takes 6 arguments. action,size,currency,underlying, and price.
* Note : something has changed with cbpro that requires debug as this stop order code does not work at
this time.
