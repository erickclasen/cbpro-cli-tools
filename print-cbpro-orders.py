'''
https://pypi.org/project/cbpro/
'''

import sys
import cbpro
import coretamodule as cm   # Core module, holds all the common code used for the ensemble of tra$

from defines import key
from defines import b64secret
from defines import passphrase


import cbpro_buy_sell as cbs
from itertools import islice

# Grab in command line args to set up the orders
# Do the fancy unpacking of the list thing to get the values out of sys.a$
try:
        this_file,action,id = sys.argv
except:
        raise Exception("Arg takes 2 arguments. action (OPEN/FILL),id (or ALL or RECENT for OPEN or product id/ order id for FILL)")
print(sys.argv)


auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)

# Get Orders has a generator as output
# All return generators
if sys.argv[1].upper() == "FILL":
        if len(sys.argv[2].upper()) > 8: # Must be an id
                #N = auth_client.get_fills(order_id=id)
                # Get 5 most recent fills by default.
                N = islice(auth_client.get_fills(order_id=id), 5)
        else:
                # Get fills for a specific order
                N = auth_client.get_fills(product_id=id)
elif sys.argv[1].upper() == 'OPEN':
        if sys.argv[2].upper() == 'ALL':
                N = auth_client.get_orders()
        elif sys.argv[2].upper() == 'RECENT':
                N = islice(auth_client.get_orders(), 5) # Get the 5 most recent open orders.
        else:
                N = auth_client.get_order(id)
else:
        raise Exception("1st arg. takes FILL or OPEN.")
# This allows the generator to print, pointer to N, sep arg into print stmt.
print(*N, sep='\n')



