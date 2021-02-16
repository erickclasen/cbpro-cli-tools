import cbpro
import csv
import time

import warnings

warnings.filterwarnings("ignore")
#ticker_filename = "/home/erick/www/btc/cbpro_crypto_price_volume_file.csv"

from defines import ticker_filename



def sleeper():
    print("XXX")
    for x in range(0,100000):
        n = 1



out_list = []

public_client = cbpro.PublicClient()
#products = public_client.get_products()
#print(products)

'''
(u'XRP', u'190', u'0.0000000000000000')
(u'BTC', u'0.0457973606767742', u'0.0000000000000000')
(u'XLM', u'0', u'0.0000000000000000')
(u'USD', u'2078.098596290176075', u'362.9480066000000000')
(u'LTC', u'0.00948174', u'0.0000000000000000')
(u'LINK', u'0', u'0.0000000000000000')
(u'ETH', u'0.06390436', u'0.0000000000000000')
(u'ETC', u'8.43436182', u'0.0000000000000000')
(u'DAI', u'7.379497077', u'0.0000000000000000')
(u'BCH', u'0.09812267', u'0.0000000000000000')
(u'ALGO', u'0', u'0.0000000000000000')

'''





# Get the product ticker for a specific product.
#print("\nBTC Ticker ---------------------------------------------------------")
''' This is the entire btc_ticker dictionary for an example to work off of {u'bid': u'6680', u'volume': u'5173.11329291', u'trade_id': 49678579, u'time': u'2018-08-26T23:16:52.652000Z', u'ask': u'6680.01', u'price': u'6680.01000000', u'size': u'0.01432357'}  '''
btc_ticker = public_client.get_product_ticker(product_id='BTC-USD')
time.sleep(0.1)
bch_ticker = public_client.get_product_ticker(product_id='BCH-USD')
time.sleep(0.1)
etc_ticker = public_client.get_product_ticker(product_id='ETC-USD')
time.sleep(0.1)
eth_ticker = public_client.get_product_ticker(product_id='ETH-USD')
time.sleep(0.1)
ltc_ticker = public_client.get_product_ticker(product_id='LTC-USD')
time.sleep(0.1)
xrp_ticker = public_client.get_product_ticker(product_id='XRP-USD')
time.sleep(0.1)
dai_ticker = public_client.get_product_ticker(product_id='DAI-USDC')
time.sleep(0.1)

# New ones as of 10/1/2019
xlm_ticker = public_client.get_product_ticker(product_id='XLM-USD')
time.sleep(0.1)

link_ticker = public_client.get_product_ticker(product_id='LINK-USD')
time.sleep(0.1)

algo_ticker = public_client.get_product_ticker(product_id='ALGO-USD')
time.sleep(0.1)

# New Ones as of 2/18/2020
atom_ticker = public_client.get_product_ticker(product_id='ATOM-USD')
time.sleep(0.1)

# New Ones as of 8/14/2020
oxt_ticker = public_client.get_product_ticker(product_id='OXT-USD')
time.sleep(0.1)

# BTC Base Currency
zec_btc_ticker = public_client.get_product_ticker(product_id='ZEC-BTC')
#print(" :",btc_ticker[])
time.sleep(0.1)

bat_ticker = public_client.get_product_ticker(product_id='BAT-USDC')
time.sleep(0.1)

cvc_ticker = public_client.get_product_ticker(product_id='CVC-USDC')
time.sleep(0.1)

gnt_ticker = public_client.get_product_ticker(product_id='GNT-USDC')
time.sleep(0.1)

mana_ticker = public_client.get_product_ticker(product_id='MANA-USDC')
time.sleep(0.1)

loom_ticker = public_client.get_product_ticker(product_id='LOOM-USDC')
time.sleep(0.1)

cgld_ticker = public_client.get_product_ticker(product_id='CGLD-USD')
time.sleep(0.1)

# 11/12/2020, OMG, OX and Kyer coins for USD and BTC trading pairs.
knc_ticker = public_client.get_product_ticker(product_id='KNC-USD')
time.sleep(0.1)
omg_ticker = public_client.get_product_ticker(product_id='OMG-USD')
time.sleep(0.1)
zrx_ticker = public_client.get_product_ticker(product_id='ZRX-USD')
time.sleep(0.1)


# 12/28/2020, OMG, OX and Kyer coins for USD and BTC trading pairs.
fil_ticker = public_client.get_product_ticker(product_id='FIL-USD')
time.sleep(0.1)
nu_ticker = public_client.get_product_ticker(product_id='NU-USD')
time.sleep(0.1)




# Grab the official cbpro timestamp and use the iso of it below.
time = public_client.get_time()

count = 0
time_out = 0
while(count < 5):

    # Print out for debugging.
    try:
        print(time['iso'],btc_ticker['price'],btc_ticker['size'],btc_ticker['volume'])
        count +=1
    except KeyError:
        print("BTC-X")
        btc_ticker = public_client.get_product_ticker(product_id='BTC-USD')
        count = 0
        sleeper()

    try:
        print(time['iso'],bch_ticker['price'],bch_ticker['size'],bch_ticker['volume'])
        count +=1
    except KeyError:
        print("BCH-X")
        bch_ticker = public_client.get_product_ticker(product_id='BCH-USD')
        count = 0
        sleeper()



    try:
        print(time['iso'],etc_ticker['price'],etc_ticker['size'],etc_ticker['volume'])
        count +=1
    except KeyError:
        print("ETC-X")
        etc_ticker = public_client.get_product_ticker(product_id='ETC-USD')
        count = 0
        sleeper()




    try: 
        print(time['iso'],eth_ticker['price'],eth_ticker['size'],eth_ticker['volume'])
        count +=1

    except KeyError:
        print("ETH-X")
        eth_ticker = public_client.get_product_ticker(product_id='ETH-USD')
        count = 0
        sleeper()


    try:    
        print(time['iso'],ltc_ticker['price'],ltc_ticker['size'],ltc_ticker['volume'])
        count +=1
  
    except KeyError:
        print("LTC-X")
        ltc_ticker = public_client.get_product_ticker(product_id='LTC-USD')
        count = 0
        sleeper()

    try:    
        print(time['iso'],xrp_ticker['price'],xrp_ticker['size'],xrp_ticker['volume'])
        count +=1
  
    except KeyError:
        print("XRP-X")
        xrp_ticker = public_client.get_product_ticker(product_id='XRP-USD')
        count = 0
        sleeper()        

    time_out+=1
    print(time_out)
    if time_out > 250:
        print("Timeout Exceeded")
        quit()


    try:
        print(time['iso'],dai_ticker['price'],dai_ticker['size'],dai_ticker['volume'])
        count +=1

    except KeyError:
        print("DAI-USDC-X")
        dai_ticker = public_client.get_product_ticker(product_id='DAI-USDC')
        count = 0
        sleeper()

    time_out+=1
    print(time_out)
    if time_out > 250:
        print("Timeout Exceeded")
        quit()


# XLM

    try:
        print(time['iso'],xlm_ticker['price'],xlm_ticker['size'],xlm_ticker['volume'])
        count +=1

    except KeyError:
        print("XLM-USD-X")
        xlm_ticker = public_client.get_product_ticker(product_id='XLM-USD')
        count = 0
        sleeper()

    time_out+=1
    print(time_out)
    if time_out > 250:
        print("Timeout Exceeded")
        quit()
# LINK

    try:
        print(time['iso'],link_ticker['price'],link_ticker['size'],link_ticker['volume'])
        count +=1

    except KeyError:
        print("LINK-USDC-X")
        link_ticker = public_client.get_product_ticker(product_id='LINK-USD')
        count = 0
        sleeper()

    time_out+=1
    print(time_out)
    if time_out > 250:
        print("Timeout Exceeded")
        quit()
# ALGO

    try:
        print(time['iso'],algo_ticker['price'],algo_ticker['size'],algo_ticker['volume'])
        count +=1

    except KeyError:
        print("ALGO-USDC-X")
        algo_ticker = public_client.get_product_ticker(product_id='ALGO-USD')
        count = 0
        sleeper()

    time_out+=1
    print(time_out)
    if time_out > 250:
        print("Timeout Exceeded")
        quit()

# ATOM

    try:
        print(time['iso'],atom_ticker['price'],atom_ticker['size'],atom_ticker['volume'])
        count +=1

    except KeyError:
        print("ATOM-USD-X")
        atom_ticker = public_client.get_product_ticker(product_id='ATOM-USD')
        count = 0
        sleeper()

    time_out+=1
    print(time_out)
    if time_out > 250:
        print("Timeout Exceeded")
        quit()


# OXT

    try:
        print(time['iso'],oxt_ticker['price'],oxt_ticker['size'],oxt_ticker['volume'])
        count +=1

    except KeyError:
        print("OXT-USD-X")
        oxt_ticker = public_client.get_product_ticker(product_id='OXT-USD')
        count = 0
        sleeper()

    time_out+=1
    print(time_out)
    if time_out > 250:
        print("Timeout Exceeded")
        quit()

# ZEC-BTC
# zec_btc_ticker
    try:
        print(time['iso'],zec_btc_ticker['price'],zec_btc_ticker['size'],zec_btc_ticker['volume'])
        count +=1

    except KeyError:
        print("ZEC-BTC-X")
        zec_btc_ticker = public_client.get_product_ticker(product_id='ZEC-BTC')
        count = 0
        sleeper()

    time_out+=1
    print(time_out)
    if time_out > 250:
        print("Timeout Exceeded")
        quit()

# BAT-USDC

    try:
        print(time['iso'],bat_ticker['price'],bat_ticker['size'],bat_ticker['volume'])
        count +=1

    except KeyError:
        print("BAT-USDC-X")
        bat_ticker = public_client.get_product_ticker(product_id='BAT-USDC')
        count = 0
        sleeper()

    time_out+=1
    print(time_out)
    if time_out > 250:
        quit()

# CVC-USDC

    try:
        print(time['iso'],cvc_ticker['price'],cvc_ticker['size'],cvc_ticker['volume'])
        count +=1

    except KeyError:
        print("CVC-USDC-X")
        cvc_ticker = public_client.get_product_ticker(product_id='CVC-USDC')
        count = 0
        sleeper()

    time_out+=1
    print(time_out)
    if time_out > 250:
        quit()


# GNT-USDC

    try:
        print(time['iso'],gnt_ticker['price'],gnt_ticker['size'],gnt_ticker['volume'])
        count +=1

    except KeyError:
        print("GNT-USDC-X")
        gnt_ticker = public_client.get_product_ticker(product_id='GNT-USDC')
        count = 0
        sleeper()

    time_out+=1
    print(time_out)
    if time_out > 250:
        quit()

        
# MANA-USDC

    try:
        print(time['iso'],mana_ticker['price'],mana_ticker['size'],mana_ticker['volume'])
        count +=1

    except KeyError:
        print("MANA-USDC-X")
        mana_ticker = public_client.get_product_ticker(product_id='MANA-USDC')
        count = 0
        sleeper()

    time_out+=1
    print(time_out)
    if time_out > 250:
        quit()


# LOOM-USDC

    try:
        print(time['iso'],loom_ticker['price'],loom_ticker['size'],loom_ticker['volume'])
        count +=1

    except KeyError:
        print("LOOM-USDC-X")
        loom_ticker = public_client.get_product_ticker(product_id='LOOM-USDC')
        count = 0
        sleeper()

    time_out+=1
    print(time_out)
    if time_out > 250:
        quit()

# CGLD-USD
    try:
        print(time['iso'],cgld_ticker['price'],cgld_ticker['size'],cgld_ticker['volume'])
        count +=1

    except KeyError:
        print("CGLD-USD-X")
        cgld_ticker = public_client.get_product_ticker(product_id='CGLD-USD')
        count = 0
        sleeper()

    time_out+=1
    print(time_out)
    if time_out > 250:
        quit()



# KNC-USD
    try:
        print(time['iso'],knc_ticker['price'],knc_ticker['size'],knc_ticker['volume'])
        count +=1

    except KeyError:
        print("KNC-USD-X")
        knc_ticker = public_client.get_product_ticker(product_id='KNC-USD')
        count = 0
        sleeper()

    time_out+=1
    print(time_out)
    if time_out > 250:
        quit()


# OMG-USD
    try:
        print(time['iso'],omg_ticker['price'],omg_ticker['size'],omg_ticker['volume'])
        count +=1

    except KeyError:
        print("OMG-USD-X")
        omg_ticker = public_client.get_product_ticker(product_id='OMG-USD')
        count = 0
        sleeper()

    time_out+=1
    print(time_out)
    if time_out > 250:
        quit()

# ZRX-USD
    try:
        print(time['iso'],zrx_ticker['price'],zrx_ticker['size'],zrx_ticker['volume'])
        count +=1

    except KeyError:
        print("ZRX-USD-X")
        zrx_ticker = public_client.get_product_ticker(product_id='ZRX-USD')
        count = 0
        sleeper()

    time_out+=1
    print(time_out)
    if time_out > 250:
        quit()        


# FIL-USD
    try:
        print(time['iso'],fil_ticker['price'],fil_ticker['size'],fil_ticker['volume'])
        count +=1

    except KeyError:
        print("FIL-USD-X")
        fil_ticker = public_client.get_product_ticker(product_id='FIL-USD')
        count = 0
        sleeper()

    time_out+=1
    print(time_out)
    if time_out > 250:
        quit()


# NU-USD
    try:
        print(time['iso'],nu_ticker['price'],nu_ticker['size'],nu_ticker['volume'])
        count +=1

    except KeyError:
        print("NU-USD-X")
        nu_ticker = public_client.get_product_ticker(product_id='NU-USD')
        count = 0
        sleeper()

    time_out+=1
    print(time_out)
    if time_out > 250:
        quit()





        
# Append the items to the outlist for saving to the CSV file.
# Time
out_list.append(time['iso'])
# Price
out_list.append(btc_ticker['price'])
out_list.append(bch_ticker['price'])
out_list.append(etc_ticker['price'])
out_list.append(eth_ticker['price'])
out_list.append(ltc_ticker['price'])

# Volumes
out_list.append(btc_ticker['volume'])
out_list.append(bch_ticker['volume'])
out_list.append(etc_ticker['volume'])
out_list.append(eth_ticker['volume'])
out_list.append(ltc_ticker['volume'])

# Newer ones, new format
#out_list.append(xrp_ticker['price'])
#out_list.append(xrp_ticker['volume'])
out_list.append(0)
out_list.append(0)

out_list.append(dai_ticker['price'])
out_list.append(dai_ticker['volume'])

# 10/1/2019
out_list.append(xlm_ticker['price'])
out_list.append(xlm_ticker['volume'])
out_list.append(link_ticker['price'])
out_list.append(link_ticker['volume'])
out_list.append(algo_ticker['price'])
out_list.append(algo_ticker['volume'])

# 02/18/2020
out_list.append(atom_ticker['price'])
out_list.append(atom_ticker['volume'])

# 08/14/2020
out_list.append(oxt_ticker['price'])
out_list.append(oxt_ticker['volume'])

out_list.append(str(float(zec_btc_ticker['price'])*float(btc_ticker['price']))) # Normalize to a ZEC-USD and let the code downstream deal with it.
out_list.append(zec_btc_ticker['volume'])

out_list.append(bat_ticker['price'])
out_list.append(bat_ticker['volume'])

out_list.append(cvc_ticker['price'])
out_list.append(cvc_ticker['volume'])

out_list.append(gnt_ticker['price'])
out_list.append(gnt_ticker['volume'])

out_list.append(mana_ticker['price'])
out_list.append(mana_ticker['volume'])

out_list.append(loom_ticker['price'])
out_list.append(loom_ticker['volume'])

out_list.append(cgld_ticker['price'])
out_list.append(cgld_ticker['volume'])

out_list.append(knc_ticker['price'])
out_list.append(knc_ticker['volume'])

out_list.append(omg_ticker['price'])
out_list.append(omg_ticker['volume'])

out_list.append(zrx_ticker['price'])
out_list.append(zrx_ticker['volume'])

out_list.append(fil_ticker['price'])
out_list.append(fil_ticker['volume'])

out_list.append(nu_ticker['price'])
out_list.append(nu_ticker['volume'])


#out_list.append(btc_ticker['size'])
#out_list.append(btc_ticker['volume'])
#print(out_list)
#quit()
# Open the CSV file and output a row using the out_list

with open(ticker_filename, mode='a') as outfile:
    output_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    output_writer.writerow(out_list)
