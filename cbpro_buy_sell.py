import cbpro
import json

#from coretamodule import clip_floor
import coretamodule as cm

from defines import key
from defines import b64secret
from defines import passphrase

ltcm_3__amount = 25.00



# https://stackoverflow.com/questions/45862777/gdax-node-b64secret


def high_limit_continue(product_label,currencies_currently_traded,btc_currencies,eth_currencies,usd_currencies,currency,underlying,underlying_avail,currency_avail,overage_allowed,portfolio_size):
        ''' If at the high limit return True to allow the code to continue. '''
        # For btc and eth which serve as underlying allow a higher limit, up to 
        # a proportion of the USD avail scaled by how many coins they are trading 
        # to all coins-pairs traded.        
        if product_label == 'BTC-USD' or product_label == 'ETH-USD':
                if product_label == 'BTC-USD': # Get the coin list for BTC pairs
                        currencies_currently_traded = btc_currencies
                else: # Now ETH pairs.
                        currencies_currently_traded = eth_currencies
                # Allow BTC and ETH to buy up to a point in proportion to coin pairs
                # that they can trade as an underlying. Fuel for other trades, basicaaly.
                if currency_avail > (len(currencies_currently_traded)/(len(btc_currencies)+len(eth_currencies)+len(usd_currencies))) * underlying_avail:
                        print(product_label+" No buy, at high limit. Cur. Avail, Und. Avail: ",currency_avail,underlying_avail)
                        return True
        elif (underlying == 'USD' or underlying == 'USDC') and currency_avail > overage_allowed * portfolio_size / (len(currencies_currently_traded) + 1):
                print(currency+" No Buy. Portfolio Mgmt. At the high limit for the portfolio size. How many currencies, Currency Avail, High Water Mark: ",len(currencies_currently_traded),currency_avail,(overage_allowed * portfolio_size / (len(currencies_currently_traded)+1)))
                return True

        return False # No continue

# LIMIT ONLY BUY & SELL
def buy_lim(auth_client,product_label,currency,underlying,currency_price_list,scaled_buy_trade_amount,currency_avail):
        ''' Buy limit only. rtn the cbpro dict from the api'''

        if (currency == 'KNC' and underlying == 'BTC') or ( currency == 'XLM' and underlying == 'BTC'): # Do to the floating point math can't do a lim order, default to mkt order here.
                # Call the cbpro buy fxn to carry out the trade via cbpro API.    
                cbpro_rtn_dict = cbpro_buy(auth_client,round(scaled_buy_trade_amount,4),product_label)
        else:
                size,buy_price,sell_price = calculate_trade_size_and_price(currency,currency_price_list[-1],scaled_buy_trade_amount,currency_avail,underlying)
                cbpro_rtn_dict = cbpro_buy_limit(auth_client,buy_price,size,product_label)

        return cbpro_rtn_dict


def sell_lim(auth_client,product_label,currency,underlying,currency_price_list,scaled_sell_trade_amount,currency_avail,unit_multiplier=1):
        ''' Sell at limit via cbpro api. Retrun the dict from cbpro.
            unit_multiplier = transaction_record[currency][0] for general-spike. 1 for tsts.py, not put in uses default '''

        if (currency == 'ZRX' and underlying == 'BTC') or (currency == 'FIL' and underlying == 'BTC') or (currency == 'NU' and underlying == 'BTC') or (currency == 'KNC' and underlying == 'BTC') or ( currency == 'XLM' and underlying == 'BTC') or (currency == 'OMG' and underlying == 'BTC'):  # Do to the floating point math can't do a lim order, default to mkt order here.
                # Sell in propotion to the counts. Call the interface to the cbpro API.
                cbpro_rtn_dict = cbpro_sell(auth_client,round(scaled_sell_trade_amount*unit_multiplier,4),product_label)
        else:
                size,buy_price,sell_price = calculate_trade_size_and_price(currency,currency_price_list[-1],scaled_sell_trade_amount*unit_multiplier,currency_avail,underlying)
                cbpro_rtn_dict = cbpro_sell_limit(auth_client,sell_price,size,product_label)

        return cbpro_rtn_dict

# LIMIT OR MKT BUY & SELL
def buy_lim_or_mkt(auth_client,product_label,currency,underlying,currency_price_list,scaled_buy_trade_amount,currency_avail):
        ''' Buy limit or mkt depending on the coins being traded. rtn the cbpro dict from the api'''

        # Low volume XXX-USDC coins are limit only trades and BAT-ETH
        if currency == 'GNT' or currency == 'MANA' or currency == 'CVC' or currency == 'DAI' or currency == 'LOOM' or (currency == 'BAT' and underlying == 'ETH') or ( currency == 'ZEC' and underlying == 'BTC'):            
                size,buy_price,sell_price = calculate_trade_size_and_price(currency,currency_price_list[-1],scaled_buy_trade_amount,currency_avail,underlying)
                cbpro_rtn_dict = cbpro_buy_limit(auth_client,buy_price,size,product_label)
        else:
                # Call the cbpro buy fxn to carry out the trade via cbpro API.    
                cbpro_rtn_dict = cbpro_buy(auth_client,round(scaled_buy_trade_amount,4),product_label) 

        return cbpro_rtn_dict


def sell_lim_or_mkt(auth_client,product_label,currency,underlying,currency_price_list,scaled_sell_trade_amount,currency_avail,unit_multiplier=1):
        ''' Sell at limit or mkt via cbpro api. Retrun the dict from cbpro.
            unit_multiplier = transaction_record[currency][0] for general-spike. 1 for tsts.py, not put in uses default '''

        # Low volume XXX-USDC coins are limit only mode.
        if currency == 'CVC' or currency == 'GNT' or currency == 'MANA' or currency == 'DAI' or currency == 'LOOM' or (currency == 'BAT' and underlying == 'ETH') or ( currency == 'ZEC' and underlying == 'BTC'):
                size,buy_price,sell_price = calculate_trade_size_and_price(currency,currency_price_list[-1],scaled_sell_trade_amount*unit_multiplier,currency_avail,underlying)
                cbpro_rtn_dict = cbpro_sell_limit(auth_client,sell_price,size,product_label)
        else:
                # Sell in propotion to the counts. Call the interface to the cbpro API.
                cbpro_rtn_dict = cbpro_sell(auth_client,round(scaled_sell_trade_amount*unit_multiplier,4),product_label)

        return cbpro_rtn_dict




def log_transaction(text_records):
    ''' Do a dump of the text records which is list of dictionaries of all the transcations, The Ticker '''
    filename = "cbpro_transaction_records.json"
    with open(filename, 'a') as f_obj:
        json.dump(text_records, f_obj)



def cbpro_sell(auth_client,amount,product_label='BTC-USD'):
    # Place a market order by specifying amount of USD to use. 
    # Alternatively, `size` could be used to specify quantity in BTC amount.
    record = auth_client.place_market_order(product_id=product_label, 
                                  side='sell', 
                                            funds=str(amount))
    log_transaction(record)
    return record

def cbpro_buy(auth_client,amount,product_label='BTC-USD'):
    # Place a market order by specifying amount of USD to use. 
    # Alternatively, `size` could be used to specify quantity in BTC amount.
    record = auth_client.place_market_order(product_id=product_label, 
                                  side='buy', 
                                            funds=str(amount))
    log_transaction(record)
    return record

def cbpro_sell_limit(auth_client,f_price,f_size,product_label='BTC-USD'):
    # Place a limit order by specifying price of asset and size to sell. 
    # Alternatively, `size` could be used to specify quantity in BTC amount.
    record = auth_client.place_limit_order(product_id=product_label,
                                  side='sell',
                                            price=str(f_price),
                                            size=str(f_size))   
    log_transaction(record)
    return record

def cbpro_buy_limit(auth_client,f_price,f_size,product_label='BTC-USD'):
    # Place a limit order by specifying price of asset and size to sell. 
    # Alternatively, `size` could be used to specify quantity in BTC amount.
    record = auth_client.place_limit_order(product_id=product_label,
                                  side='buy',
                                            price=str(f_price),
                                            size=str(f_size))   
    log_transaction(record)
    return record




def product_selector(mode_flag):
    ''' Helper function. Takes in the mode flag amd picks out the correct currency from the list.
        Then make a tranaction. Returhns a product_label that cbpro understands.'''
    if mode_flag["Currency"] == "BTC":
        product_label = 'BTC-USD'
    elif mode_flag["Currency"] == "BCH":    
        product_label = 'BCH-USD'
    elif mode_flag["Currency"] == "ETC":    
        product_label = 'ETC-USD'
    elif mode_flag["Currency"] == "ETH":    
        product_label = 'ETH-USD'
    elif mode_flag["Currency"] == "LTC":    
        product_label = 'LTC-USD'
    else:
        print("TRAP: Bad Mode Flag, for Currency in cbpro_buy_sell in cbpro_transact function!!!")
        quit()

    return product_label        

def cbpro_transact(type,best_bank,mode_flag):
    auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)

    test = ''
    multiplier = 1
        
    # Do a translation from the mode_flag for currency to the product label for CBPRO.
    product_label = product_selector(mode_flag)

    # Scale the best_bank into an amount to buy and sell. In this way the winners get larger play in the game.
    # Reinforcment trading. Only trade products that are above water, as in showing a profit over the short time cycle.
    # Trade must always be great than $10, or else... {'message': 'funds is too small. Minimum size is 10'}
    # Check out the wording on that message!
    # Using 88 insures that the rounding using the 0.9 * (100-12) = 10.8 meets the minimum for a transaction.
    # If the bank >= 100 allow buying and selling in proportion to the best_bank, with a minimum of 12 for buy and 10.8 for sell.
    # Else if best_bank < 100 and we are selling, sell off the minimum amount of 10.
    # Else if best_bank < 100 and we are trying to buy, do nothing!
    # All others pass through and hit the trap for bad type.
    # BESTBANK  
    if best_bank > 107:
        amount = ltcm_3__amount * multiplier
    else:
        type = 0
        amount = 0

 
    # Have a multiplier of 1.2 in case profit was made, this is a guess.
    if type == -1 or type == -2:
        #test = cbpro_sell(auth_client,(round(1.2*amount,2)),product_label)
        test = cbpro_sell(auth_client,round(amount,2),product_label)
    elif type == 1:
        #test = cbpro_buy(auth_client,round(amount,2),product_label)
        test = cbpro_buy(auth_client,round(amount,2),product_label)
    elif type == 0:
        pass
    else:    
        print("TRAP: Bad Type")
        quit()


    return test


def cbpro_transact_direct_fake(type,amount,mode_flag):
    auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)

    test = ''
        
    # Do a translation from the mode_flag for currency to the product label for CBPRO.
    product_label = product_selector(mode_flag)

 
    # Directly Buy and Sell, passing the amount directly to the buy and sell functions.
    # type of -2 is an emergency stop, which will cancel all orders and sell out the positions. The amount fed in must be higher than holdings!
    if type == -1:
        test = {'Trans':'SELL','type':type,'amount':amount,'product':product_label}
    elif type == -2:
        test = {'Trans':'STOP','type':type,'amount':amount,'product':product_label}
        print("TEST: Hit Emergency Stop",test,amount)
        #test = cbpro_sell(auth_client,(round(amount,2)),product_label)
    elif type == 1:
        test = {'Trans':'BUY','type':type,'amount':amount,'product':product_label}
    elif type == 0:
        pass
    else:    
        print("TRAP: Bad Type")
        quit()


    return test

def cbpro_transact_direct(type,amount,mode_flag):
    auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)

    test = ''
        
    # Do a translation from the mode_flag for currency to the product label for CBPRO.
    product_label = product_selector(mode_flag)

 
    # Directly Buy and Sell, passing the amount directly to the buy and sell functions.
    # type of -2 is an emergency stop, which will cancel all orders and sell out the positions. The amount fed in must be higher than holdings!
    if type == -1:
        test = cbpro_sell(auth_client,(round(amount,2)),product_label)
    elif type == -2:
        test = auth_client.cancel_all(product_label)
        print("TEST: Hit Emergency Stop",test,amount)
        test = cbpro_sell(auth_client,(round(amount,2)),product_label)
    elif type == 1:
        test = cbpro_buy(auth_client,round(amount,2),product_label)
    elif type == 0:
        pass
    else:    
        print("TRAP: Bad Type")
        quit()


    return test

def cbpro_transact_direct_limit(type,price,size,mode_flag):
    auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)

    test = ''
        
    # Do a translation from the mode_flag for currency to the product label for CBPRO.
    product_label = product_selector(mode_flag)

 
    # Directly Buy and Sell, passing the amount directly to the buy and sell functions.
    # type of -2 is an emergency stop, which will cancel all orders and sell out the positions. The amount fed in must be higher than holdings!
    if type == -1:
        test = cbpro_sell_limit(auth_client,price,size,product_label)
    elif type == -2:
        test = auth_client.cancel_all(product_label)
        print("TEST: Hit Emergency Stop",test,amount)
        test = cbpro_sell_limit(auth_client,price,size,product_label)

    elif type == 1:
        test = cbpro_buy_limit(auth_client,price,size,product_label)
    elif type == 0:
        pass
    else:    
        print("TRAP: Bad Type")
        quit()

    return test
        
def cbpro_read_available(key=key,b64secret=b64secret,passphrase=passphrase):
    ''' Read in the amounts available, this can be called before a trade to make sure there is some available before a sell.
        As CBPro now has multiple portfolios to trade in with a number of key,secret and passphrases. Added optional
        params to this. Called with nothing it uses the default portfolio. Called with optional parameters allowd access to
        other portfolios. '''
    auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)

    accts = ''
    available_dict = {'BCH':0,'BTC':0,'ETC':0,'ETH':0,'LTC':0,'USD':0,'XRP':0}
    accts = auth_client.get_accounts()
    
    #print(accts)
    # Walk through dictionaries and map the amounts available into the locally used available_dict for easy use.        
    for j in range(0,len(accts)):
        #print(accts[j]['currency'],accts[j]['available'],accts[j]['hold'])
        available_dict[accts[j]['currency']] = accts[j]['available']

    return available_dict

def cbpro_read_holds(key=key,b64secret=b64secret,passphrase=passphrase):
    ''' Read in the amounts on hold in orders, this can be called before a trade to make sure there if there is a lot holding.
        This way it does not overbuy a particular asset. 
        As CBPro now has multiple portfolios to trade in with a number of key,secret and passphrases. Added optional
        params to this. Called with nothing it uses the default portfolio. Called with optional parameters allowd access to
        other portfolios. '''
    auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)

    accts = ''
    holds_dict = {'BCH':0,'BTC':0,'ETC':0,'ETH':0,'LTC':0,'USD':0,'XRP':0}
    accts = auth_client.get_accounts()

    #print(accts)
    # Walk through dictionaries and map the amounts available into the locally used available_dict for easy use.        
    for j in range(0,len(accts)):
        #print(accts[j]['currency'],accts[j]['available'],accts[j]['hold'])
        holds_dict[accts[j]['currency']] = accts[j]['hold']

    return holds_dict


def cbpro_transact_testing(type,best_bank,product_label='BTC-USD'):
    auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)

    test = ''

    # Scale the best_bank into an amount to buy and sell. In this way the winners get larger play in the game.
    # Reinforcment trading. Only trade products that are above water, as in showing a profit over the short time cycle.
    # Trade must always be great than $10, or else... {'message': 'funds is too small. Minimum size is 10'}
    # Check out the wording on that message!
    if best_bank >= 100:
        amount = best_bank - 88
    else:
        # Force a passthrough
        type = 0

    print(amount)
    #quit()
    if type == -1 or type == -2:
        test = cbpro_sell(auth_client,(0.9*amount),product_label)
    elif type == 1:
        test = cbpro_buy(auth_client,amount,product_label)
    elif type == 0:
        pass
    else:    
        print("TRAP: Bad Type")
        quit()


    return test



def calculate_trade_size_and_price(currency,currency_price,trade_amount,currency_avail=None,underlying='USD'):
    ''' For limit orders the size and price must be calculated and rounded properly for the traded currency.
        1. Also push out the bounds slightly allowing the order to rest above a sell price and below a buy price slightly.
        2. When not holding anything allow a 10% extra buy in to fill, this is mostly for algos with stop losses, in case
           price drifts down to the stop there is margin in there to avoid insufficent funds on a sale at lower price. 
                optional parameter, ignores it if not there.
        3. BTC has a lower limit of 0.001 so enforce this floor on order size.'''


    # Selling currency as related to the amount of USD.
    size = trade_amount / currency_price

    # Print the scaled value.
    print(currency+" Trade Amount: ",trade_amount)
    print(currency+" Trade Size: ",size)


    # If there is nothing in the currency, get extra to cover the costs on the first time.
    if currency_avail == 0:
            size = size * 1.1  # 10% should cover it.

  # Testing these slight pushouts that should move the limit orders slightly out of range, so that they
    # tend to have a delay in the sale, making them marmket maker orders more often than not.
    buy_pushout = 0.999
    sell_pushout = 1.001

    if currency == 'ALGO' or currency == 'OXT': # USD ONLY
            # Whole unit Min.
            
            size_accuracy = 0
            size_floor = 1
            price_accuracy = 4
    elif currency == 'CGLD' or currency == 'KNC' or currency == 'OMG':
            # Whole unit Min.

            size_accuracy = 1
            size_floor = 1
            if underlying == 'USD' or underlying == 'USDC':
                price_accuracy = 4
            else:
                price_accuracy = 8

    elif currency == 'XRP' or currency == 'NU':
                
            # 10 unit Min.
            size_accuracy = 0
            size_floor = 10
            if underlying == 'USD' or underlying == 'USDC':
                price_accuracy = 4
            else:
                price_accuracy = 8

    elif currency == 'LINK' or currency == 'DAI': # DAI is 6 units price accuracy and 5 for size, but this is close enough to work for it.
            size_accuracy = 2
            size_floor = 1.0

            if underlying == 'USD' or underlying == 'USDC':
                price_accuracy = 5
            else:
                price_accuracy = 8
    elif currency == 'BAT' or currency == 'CVC' or currency == 'GNT' or currency == 'MANA' or currency == 'LOOM' or currency == 'XLM':
            # Whole unit Min.
            size_accuracy = 0  
            size_floor = 1

            if underlying == 'USD' or underlying == 'USDC':
                price_accuracy = 6
            else:
                price_accuracy = 8
    elif currency == 'ATOM':

            size_accuracy = 1 # 3 for etc 1 for atom
            size_floor = 0.1 # ATOM is 0.1 floor 0.01 for etc
            if underlying == 'USD' or underlying == 'USDC':
                price_accuracy = 3
            else:
                price_accuracy = 6 #8
    elif currency == 'ETC':

            size_accuracy = 3 # 3 for etc 1 for atom
            size_floor = 0.01 # ATOM is 0.1 floor 0.01 for etc
            if underlying == 'USD' or underlying == 'USDC':
                price_accuracy = 3
            else:
                price_accuracy = 6 #8
    elif currency == 'LTC':

            size_accuracy = 3
            size_floor = 0.1
            if underlying == 'USD' or underlying == 'USDC':
                price_accuracy = 2
            else:
                price_accuracy = 6 #8
    elif currency == 'BTC':   # Size to three, prices to 2 places.
            # Set a floor as BTC can go less than 0.001 in size.
            size_accuracy = 3  
            size_floor = 0.001
            price_accuracy = 2
    elif currency == 'ZEC': 

            size_accuracy = 3
            size_floor = 0.01
            if underlying == 'USD' or underlying == 'USDC':
                price_accuracy = 2
            else:
                price_accuracy = 6
    elif currency == 'ETH' or currency == 'BCH':

            size_accuracy = 2 # I think this is OK
            size_floor = 0.01
            if underlying == 'USD' or underlying == 'USDC':
                price_accuracy = 2
            else:
                price_accuracy = 5

    else:
            # Catchall ,may or may not work in all case in the future.
            size_accuracy = 2
            size_floor = 0.01
            price_accuracy = 2
            #raise Exception("Unsupported Currency for Limit Order.")   


    # Create a size and price that it acceptable for the CBPRO exchange. 
    # Both the price and size have accuracy requirements and the size has a minimum floor.
        
    size = round(cm.clip_floor(size,size_floor),size_accuracy)
    buy_price = round(buy_pushout * currency_price,price_accuracy)
    sell_price = round(sell_pushout * currency_price,price_accuracy)


    print(currency+" size and  trade amount in USD: ",size,size*currency_price) 

    return size,buy_price,sell_price


def cbpro_limit_order_gtt(auth_client,side,f_price,f_size,cncl_aftr='hour',product_label='BTC-USD'):
    '''Place a limit order by specifying price of asset and size to sell. 
       Alternatively, `size` could be used to specify quantity in BTC amount.'''
    record = auth_client.place_limit_order(product_label,
                                  side,
                                  price=str(f_price),
                                  size=str(f_size),
                                  time_in_force='GTT',
                                  cancel_after=cncl_aftr)
    return record



#------------ MAIN FOR TESTING ---------------------------

#import pprint


#const apiURI = 'https://api.gdax.com';
#const sandboxURI = 'https://api-public.sandbox.gdax.com';



# Use the sandbox API (requires a different set of API access credentials)
#auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase,
#                                  api_url="https://api-public.sandbox.pro.coinbase.com")

#print("The Accounts\n\n")
#test = auth_client.get_accounts()
#print(test)

#pp = pprint.PrettyPrinter(width=210)
#pp.pprint(test)



#test = cbpro_transact_testing(1,125,'BCH-USD')

#print("The Tranaction Record\n\n")
#pp = pprint.PrettyPrinter(width=210)
#pp.pprint(test)


#------------------------------- Trading Notes ---------------------------------
# This code did well so far buying and sell $10 at a time, so now is...
# cbpro under test with the reinforced trading.
# $511.10 on 9-06-2018

