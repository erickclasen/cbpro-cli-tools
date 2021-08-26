#!/usr/bin/python
#title			:manual-portfolio-adjust-using-default-keys.py
#description	:This code is a hack of the index-balancer.py code from cbpro-index-fund-algo 
# that allows a manual sell or buy of assets # it will buy and sell to a specific amount.
# It requires the defines.py file which holds the key,b64secret and passphrase for CBPro API..
# It is a tool to manually manage a portfolio from the command line.
#author			:Erick Clasen
#date			:20210822
#version		:0.1
#usage			:python3 manual-portfolio-adjust-using-default-keys.py buy/sell amount highlimit
#			Where buy amd sell are spelled out and the amount is the amount to asjust all assets to
#			The highlimit is the amount above which no action should be taken.
#			For example if the following is executed...
#
#			python3 manual-portfolio-adjust-using-default-keys.py sell 20 999
#
#			... the above command will sell all assets holding above $20 and below $999 to $20.
#			It will produce a log file called manual-portfolio-adjust-using-default-keys.py.log
#			This will log all the transactions.

#notes			:
#python_version	: 2.7.6
#python_version	: Python 3.4.3
#==============================================================================
this_file = "cbpro_index_fund_algo.py"

import cbpro
import pprint
import json
import csv
import sys
import time
import coretamodule as cm   # Core module, holds all the common code used for the ensemble of trading algorithms
import cbpro_buy_sell as cbs


from defines import ticker_filename

from defines import key
from defines import b64secret
from defines import passphrase

from datetime import datetime

this_file = sys.argv[0] #"index-balancer.py"



def record_round_trip_transaction(time_string,action,currency,underlying,currency_price,asset_held,idx_target,trade_amount,index_value,trans_string):

    out_list = []

    # Summary File Name, all in one log.
    sfilename = "summary-"+this_file+".log"

    # Record it...

    if action == 'SELL':
        filename = "manual-rebal-sell-"+underlying[1]+".log"
    elif action == 'BUY':
        filename = "manual-rebal-buy-"+underlying[0]+".log"
    else:
        raise Exception("BAD BS FLAG")

    # Logs are stored in a standard format of time,action (BUY or SELL) and the currency price. This is follo$
    #and lastly the dictionaries, that the exchange reports back.

    out_list.append(time_string)
    out_list.append(action)
    out_list.append(currency+"-"+underlying[0]+":"+underlying[1])
    out_list.append(str(round(currency_price,10)))
    out_list.append(str(round(asset_held,2)))
    out_list.append(str(round(idx_target,2)))
    out_list.append(str(round(trade_amount,2)))
    out_list.append(str(round(index_value,2)))

    # If there is a message from cbpro, show it.
    if 'message' in trans_string:
        out_list.append(trans_string)


    #Open the CSV file and output a row using the out_list
    with open(filename, mode='a') as outfile:
        output_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(out_list)

    # Ditto for summary log file.
    with open(sfilename, mode='a') as outfile:
        output_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(out_list)


    out_list.append("")
    out_list.append("")
    out_list.append("                     ")
    out_list.append(trans_string)



    # Open the CSV file and output a row using the out_list
    with open('verbose-'+filename, mode='a') as outfile:
        output_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(out_list)



def cbpro_read_available(price_dict,auth_client):

    accts = ''

    # Keeping score with these vars which will be running totals
    total_avail = 0
    total_held = 0

    accts = auth_client.get_accounts()

    #print(accts)
    #quit()     
    # Header
    asset_dict = {}   

    print("")
    print('Currency',' Price',"\t", 'Available',' Hold',"\t",'Avail in USD',' Held in USD')
    
    for j in range(0,len(accts)):


        # If not a fiat, then calculate the availavle and held and make a running total.
        # Then print out a formatted summary.
        if accts[j]['currency'] != 'USDC' and accts[j]['currency'] != 'USD':

                try:
                        asset_avail = price_dict[accts[j]['currency']+" Price"] * float(accts[j]['available'])
                except KeyError:
                        continue

                asset_held = price_dict[accts[j]['currency']+" Price"] * float(accts[j]['hold'])
                total_avail += asset_avail
                total_held += asset_held

                if asset_held > 0:               
                        print(accts[j]['currency'],round(price_dict[accts[j]['currency']+" Price"],6),"\t\t", round(float(accts[j]['available']),2),round(float(accts[j]['hold']),2),"\t\t\t",round(asset_avail,2),round(asset_held,2))
                else:
                        print(accts[j]['currency'],round(price_dict[accts[j]['currency']+" Price"],6),"\t\t", round(float(accts[j]['available']),2),round(float(accts[j]['hold']),2),"\t\t\t",round(asset_avail,2))



        else: # SPecial case for FIAT's where the price is a unit of 1 and not read in at all from the price list of dicts.   
            print(accts[j]['currency'],"\t\t\t",round(float(accts[j]['available']),2),round(float(accts[j]['hold']),2))
            asset_avail = float(accts[j]['available'])
            asset_held = float(accts[j]['hold'])
            total_avail += asset_avail
            total_held += asset_held            

        # Total tied to asset.
        total_for_asset = asset_avail # + asset_held, can't use asset held, gets it out of balance.
        # Save it in a dictionary for use later on in the main code to adjust from.
        asset_dict[accts[j]['currency']] = total_for_asset 
        
    # Print out a summary of the available and held and the total
    print("")
    print("Total Available in USD: ",round(total_avail,2))
    print("Total Held in USD: ",round(total_held,2))
    print("Portfolio Size in USD: ",round(total_held+total_avail,2))
    print("Average size of asset in USD",round((total_held+total_avail)/len(accts),2))  
    return round(total_held+total_avail,2),asset_dict


def cbpro_limit_order_gtt_1(auth_client,side,f_price,f_size,product_label='BTC-USD'):
    '''Place a limit order by specifying price of asset and size to sell. 
       Alternatively, `size` could be used to specify quantity in BTC amount.'''
    record = auth_client.place_limit_order(product_label,
                                  side,
                                  price=str(f_price),
                                  size=str(f_size),
                                  time_in_force='GTT',
                                  cancel_after='hour')
    return record

def index_value_get(price_list):
        ''' Take in a list of prices and compute the index value as a basket of assets. '''
        # The index scaler as calculated on 02/01/2021 via the index-scaler.py code
        index_scaler = {'BTC': 1.2948351898809769e-06, 'BCH': 0.00010715265395693321, 'ETC': 0.005779378023337128, 'ETH': 3.303819215012555e-05, 'LTC': 0.0003332689013457398, 'DAI': 0.04345870445256156, 'XLM': 0.1368368305634366, 'LINK': 0.0019502758831010096, 'ALGO': 0.06871860418771174, 'ATOM': 0.005323651386012638, 'OXT': 0.12584156546907443, 'ZEC': 0.000498396916813309, 'BAT': 0.14554708164274333, 'CVC': 0.2871046102971217, 'GNT': 0.2645354981507646, 'MANA': 0.2889746629905236, 'LOOM': 0.6658232904987016, 'CGLD': 0.015614947877303985, 'KNC': 0.03362587847607519, 'OMG': 0.012470818285212602, 'ZRX': 0.06480732296826613, 'FIL': 0.001938890438924079, 'NU': 0.14377731769036117}
        index_value = 0
        for key in index_scaler:
                #print(price_dict[key+" Price"]*new_dict[key]) # Debug
                index_value += price_list[key+" Price"]*index_scaler[key]

        return index_value

# --------------- main. ----------------            
BUY_THRESHOLD_SCALER = 0.9
SELL_THRESHOLD_SCALER = 1.1
ORDER_AMT_SCALER = 0.97

price_list_of_dicts = cm.read_lines_from_csv_file(ticker_filename)

current_prices = price_list_of_dicts[-1]
print(current_prices)

# Get teh index value and show it.
index_value = index_value_get(current_prices)
print("\nIndex Value:",round(index_value,2))

# Authorize with keys...
auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)

# What is the total amount of assets held in USD. Asset dict is the holds by individual asset.
total,asset_dict = cbpro_read_available(current_prices,auth_client)

# XRP is MIA from now on.
print("\nRemove XRP and DAI")
del asset_dict['XRP']
del asset_dict['DAI']

print("\n\n-----Index Fund Balancing-----\n")
# DO a sanity check
print("\n\nTotal by regular calc vs total by sum of dict values:",total,sum(asset_dict.values()),"\n",asset_dict)

# Create a 'sort of' target that has ALL in, including USDC.
idx_target = total/len(asset_dict)
print("\nPrint Target (with USD+USDC) and How Many Assets:",round(idx_target,2),len(asset_dict))

# Remove the underlying's after daving the amounts off to check for availability when making a trade
usd_avail = asset_dict['USD']
usdc_avail = asset_dict['USDC']
print("\nUSD and USDC Available:",round(usd_avail,2), round(usdc_avail,2))

# Remove USDC that way USD is the only underlying present in the target calculation
del asset_dict['USDC']

print("\nHow much in holds including USD: ",round(sum(asset_dict.values()),2))

# Get the real target, with USD only and the cryptos in it.
idx_target = sum(asset_dict.values())/(len(asset_dict)+1) # ??? plus 1 ???
#idx_target = sum(asset_dict.values())/len(asset_dict)
print("\nPrint Target (with USD) and How Many Assets:",round(idx_target,2),len(asset_dict))

# Now remove USD as we can't self trade with it.
del asset_dict['USD']

# Primary list of coins that   MUST   trade under USDC.
usdc_list_manditory = ['BAT','CVC','GNT','LOOM','MANA']
# Expanded list of coins that   CAN   trade under USDC.
usdc_list_optional = ['BTC','ETH','ZEC']
print("\nTrading via USDC underlying: ",usdc_list_manditory,usdc_list_optional)

# Find the ratio of the count of the assets that are trading #USDC/USD and how
# much is available in each one to trade.
usdc_asset_len = len(usdc_list_manditory) + len(usdc_list_optional)
usdc_usd_asset_count_ratio = usdc_asset_len/(len(asset_dict)-usdc_asset_len) # The ratio of USDC assets to USD, a count
usdc_usd_avail_ratio = usdc_avail/usd_avail # Ratio of amounts avail.
print("\nRatios, USDC/USD counts and USDC/USD avail",round(usdc_usd_asset_count_ratio,2),round(usdc_usd_avail_ratio,2))
print() # Whitespace


#del asset_dict['BTC'] # BTC @ 0.001 is to big of a trade now, do it manually, not by algo.


# Hack to allow the index scaler code to allow a manual override to buy or sell to a set level.
this_file,action_allowed,idx_target_str,asset_high_limit = sys.argv
idx_target = float(idx_target_str)
print("\nProceed with "+action_allowed.upper()+" to new target amount at",idx_target)
print("\nonly on assets holding less than:",asset_high_limit)
print("\n\tCtrl-C to exit...\n")
# Delay to allow a cancel...
time.sleep(5.5)    # Pause 5.5 seconds


# The work starts here
for asset in asset_dict:

        # IF it is holding too much just quit.
        if asset_dict[asset] > int(asset_high_limit):
                print(asset+" holding above high limit, NOOP \t asset $ amount and high limit:",round(asset_dict[asset],2),asset_high_limit)
                continue


        if asset in usdc_list_optional:
                #if usdc_usd_asset_count_ratio < usdc_usd_avail_ratio:
                #        underlying = ("USDC","USD") # SCALE IN
                #        underlying_avail = usdc_avail # Buy via USDC
                #        print("\tScale IN")
                #else:
                #        underlying = ("USD","USDC") # SCALE OUT
                #        underlying_avail = usd_avail # Buy via USD.
                #        print("\tScale OUT")

                # Force this for the manual override!
                #underlying = ("USDC","USDC") # Normal
                #underlying_avail = usdc_avail # Buy via USDC

                underlying = ("USD","USD") # Only if all into USD
                underlying_avail = usd_avail # Buy via USD.


        elif asset in usdc_list_manditory:
                underlying = ("USDC","USDC")
                underlying_avail = usdc_avail
        else:
                underlying = ("USD","USD")
                underlying_avail = usd_avail


        current_price = current_prices[asset+" Price"]


        if action_allowed.upper() == 'BUY' and asset_dict[asset] < idx_target * BUY_THRESHOLD_SCALER:
                action = "BUY"
                print(asset,round(asset_dict[asset],2),"\t",action)
                trade_amount = (idx_target - asset_dict[asset]) * ORDER_AMT_SCALER

        elif action_allowed.upper() == 'SELL' and asset_dict[asset] > idx_target * SELL_THRESHOLD_SCALER:
                action = "SELL"

                print(asset,round(asset_dict[asset],2),"\t",action)
                trade_amount = (asset_dict[asset]  - idx_target) * ORDER_AMT_SCALER
        else: # NOOP
                print(asset,round(asset_dict[asset],2))
                action = "" # NOOP


        
        # At this point do a buy or sell.
        if action == 'BUY':
            # Check if enough underlying is available.
            if underlying_avail < trade_amount:
                    print("Not enough "+underlying+" available, break! ",underlying_avail)
                    continue
            size,buy_price,sell_price = cbs.calculate_trade_size_and_price(asset,current_prices[asset+" Price"],trade_amount,asset_dict[asset])
            #cbpro_rtn_dict = cbs.cbpro_buy_limit(auth_client,buy_price,size,asset+"-"+underlying)
            cbpro_rtn_dict =  cbpro_limit_order_gtt_1(auth_client,action.lower(),buy_price,size,asset+"-"+underlying[0])

        elif action == 'SELL':
            # Check if enough underlying is available.
            if asset_dict[asset] < trade_amount:
                    print("Not enough "+asset+"-"+underlying+" available, break! ",underlying_avail)
                    continue
            size,buy_price,sell_price = cbs.calculate_trade_size_and_price(asset,current_prices[asset+" Price"],trade_amount,asset_dict[asset])
            #cbpro_rtn_dict = cbs.cbpro_sell_limit(auth_client,sell_price,size,product_label)
            cbpro_rtn_dict =  cbpro_limit_order_gtt_1(auth_client,action.lower(),sell_price,size,asset+"-"+underlying[1])
        # If action is active, some transaction occured, record it.
        if action != "":
                record_round_trip_transaction(str(datetime.now()),action,asset,underlying,current_price,asset_dict[asset],idx_target,trade_amount,index_value,cbpro_rtn_dict)



# Save this to be used by the records.

with open("portfolio_size.json", 'w') as f_obj:
    json.dump(total,f_obj)


#print(a)
# Format example
''' {u'available': u'0', u'balance': u'0.0000000000000000', u'profile_id': u'c9dbb516-181c-4f76-89c0-37cc63f41004', u'currency': u'BCH', u'hold': u'0.0000000000000000', u'id': u'a7667476-1207-4ed6-a1a7-fa5cf64c34cd'}
 '''

'''
0(u'LTC', u'0', u'0.0000000000000000')
1(u'BTC', u'0.0122494', u'0.0300000000000000')
2(u'USD', u'366.4013870112286', u'0.0000000000000000')
3(u'ETH', u'0.42951279', u'0.0000000000000000')
4(u'ETC', u'2.05145879', u'0.0000000000000000')
5(u'BCH', u'0', u'0.0000000000000000')

'''
