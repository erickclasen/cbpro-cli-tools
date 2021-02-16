'''
https://pypi.org/project/cbpro/
'''

import cbpro
import coretamodule as cm   # Core module, holds all the common code used for the ensemble of tra$
#import json
import csv
from datetime import datetime
#import copy
#import os

from defines import key
from defines import b64secret
from defines import passphrase
#from defines import portfolio_size

#import cbpro


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
# CANCEL ORDERS

# Grab in command line args to set up the orders
# Do the fancy unpacking of the list thing to get the values out of sys.argv.
try:
        this_file,currency,underlying,order = sys.argv
except:
        raise Exception("Arg takes 3 arguments. currency,underlying, and order code or all")
print(sys.argv)

product_label = currency.upper()+"-"+underlying.upper()

# Auth up here as it is used next to confirm.
auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)

# Print out the order to confirm. This will also confirm.
if order != "all":
	print()
	print(auth_client.get_order(order))
	print()
else:
	print("Set to cancel ALL ORDERS for "+product_label)
# Confirm the action by asking for user input.
print("\n\ncancel "+order+" of "+product_label)

print("\nY to confirm, anything else to quit.\n")
if input().upper() != "Y":
        quit()

# Go ahead and place the order. There is no check on amounts available, up to the user to
# Determine if there is enough $.

if order.lower() == "all":
	cbpro_rtn_dict = auth_client.cancel_all(product_id=product_label)
else:
	cbpro_rtn_dict = auth_client.cancel_order(order)


print()
print(cbpro_rtn_dict) # Show the return msg from cbpro.

# Record this for the future, also for the ID in case order is to be
# cancelled, need code for this TBD.
record_trans_record(this_file,cbpro_rtn_dict,order,product_label,0,0)
