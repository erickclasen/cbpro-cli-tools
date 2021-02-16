'''
https://pypi.org/project/cbpro/
'''

import cbpro
import coretamodule as cm   # Core module, holds all the common code used for the ensemble of tra$

import csv
from datetime import datetime

from defines import key
from defines import b64secret
from defines import passphrase


import cbpro_buy_sell as cbs
import sys


def record_trans_record(this_file,cbpro_rtn_dict,action,product_label,price,size):
        ''' Take in values to be recorded in a log file of the transaction for
            a permanent record of the action. Takes in the required values and
            saves into a CSV log file.
        '''

        out_list = []
        filename = this_file+".log"

        out_list.append(str(datetime.now()))
        out_list.append(product_label)
        out_list.append(action)

        out_list.append(price)
        out_list.append(size)
        out_list.append(cbpro_rtn_dict)


        #Open the CSV file and output a row using the out_list
        with open(filename, mode='a') as outfile:
                output_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                output_writer.writerow(out_list)



#------------------------------ MAIN. ---------------------------------
# LIMIT ONLY BUY & SELL

# Grab in command line args to set up the orders
# Do the fancy unpacking of the list thing to get the values out of sys.argv.
try:
        this_file,action,size,currency,underlying,price = sys.argv
except:
        raise Exception("Arg takes 6 arguments. action,size,currency,underlying, and price")
print(sys.argv)

product_label = currency.upper()+"-"+underlying.upper()

# Confirm the action by asking for user input.
print("\n\n"+action.title()+" "+size+" of "+product_label+" at "+price)
print("\nThe total order in USD is:",round(float(price)*float(size),2))

print("\nY to confirm, anything else to quit.\n")
if input().upper() != "Y":
        quit()

# Go ahead and place the order. There is no check on amounts available, up to the user to
# Determine if there is enough $.

auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)

if action.lower() == "buy":
        cbpro_rtn_dict = cbs.cbpro_buy_limit(auth_client,price,size,product_label)

elif action.lower() == "sell":
        cbpro_rtn_dict = cbs.cbpro_sell_limit(auth_client,price,size,product_label)

print()
print(cbpro_rtn_dict) # Show the return msg from cbpro.


# Record this for the future, also for the ID in case order is to be
# cancelled, need code for this TBD.
record_trans_record(this_file,cbpro_rtn_dict,action.upper(),product_label,price,size)
