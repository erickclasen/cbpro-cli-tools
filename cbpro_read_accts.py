import cbpro
import pprint
import json


import coretamodule as cm   # Core module, holds all the common code used for the ensemble of trading algorithms


from defines import ticker_filename

from defines import key
from defines import b64secret
from defines import passphrase


def cbpro_read_available(price_dict):
    auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)

    accts = ''

    available_dict = {'BCH':0,'BTC':0,'ETC':0,'ETH':0,'LTC':0,'USD':0,'XRP':0}

    # Keeping score with these vars which will be running totals
    total_avail = 0
    total_held = 0

    accts = auth_client.get_accounts()


    # Header
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
        
    # Print out a summary of the available and held and the total
    print("")
    print("Total Available in USD: ",round(total_avail,2))
    print("Total Held in USD: ",round(total_held,2))
    print("Portfolio Size in USD: ",round(total_held+total_avail,2))
    print("Average size of asset in USD",round((total_held+total_avail)/len(accts),2))  
    return round(total_held+total_avail,2)


def index_value_get(price_list):
        ''' Take in a list of prices and compute the index value as a basket of assets. '''
        # The index scaler as calculated on 02/01/2021 via the index-scaler.py code
        index_scaler = {'BTC': 1.2948351898809769e-06, 'BCH': 0.00010715265395693321, 'ETC': 0.005779378023337128, 'ETH': 3.303819215012555e-05, 'LTC': 0.0003332689013457398, 'DAI': 0.04345870445256156, 'XLM': 0.1368368305634366, 'LINK': 0.0019502758831010096, 'ALGO': 0.06871860418771174, 'ATOM': 0.005323651386012638, 'OXT': 0.12584156546907443, 'ZEC': 0.000498396916813309, 'BAT': 0.14554708164274333, 'CVC': 0.2871046102971217, 'GNT': 0.2645354981507646, 'MANA': 0.2889746629905236, 'LOOM': 0.6658232904987016, 'CGLD': 0.015614947877303985, 'KNC': 0.03362587847607519, 'OMG': 0.012470818285212602, 'ZRX': 0.06480732296826613, 'FIL': 0.001938890438924079, 'NU': 0.14377731769036117}
        index_value = 0
        for key in index_scaler:
                #print(price_dict[key+" Price"]*new_dict[key]) # Debug
                index_value += price_list[key+" Price"]*index_scaler[key]

        return index_value


# --------------- main ----------------            


price_list_of_dicts = cm.read_lines_from_csv_file(ticker_filename)
print(price_list_of_dicts[-1])

print("\nIndex Value:",round(index_value_get(price_list_of_dicts[-1]),2))
total = cbpro_read_available(price_list_of_dicts[-1])

# Save this to be used by the trading programs.

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
