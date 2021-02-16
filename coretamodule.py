import csv
import json
from cbpro_buy_sell import cbpro_read_available
from cbpro_buy_sell import cbpro_read_holds


''' Core Technical Analysis Module
    This module contains the core shared functions for the following code.
    ichimoku-trader.py
    ltcm.py
    pairs+mrt-fractal
    de-mrt
    mrt-fractal with fixed lookback of 10.

    The idea is to centralize a lot of common code, making for better readability and functions that can be updated in one place.

'''


def rsi(price_list,lookback=14):
    ''' Function taken from p363, New Trading Systems and Methods by Kaufmann, 4th ED. The pseudocode listed was almost a drop in. This code is simplified
        and does not use the averaging off method to create the RSI as described on p362. '''
    sumup = 0
    sumdn = 0

    # Need to range out from 2 to the lookback + 2 otherwise -i+1 will equal zero at the start and grab the first elelmet of the list.    
    for i in range(2,int(lookback+2)):
        if price_list[-i] - price_list[-i+1] > 0: # Is the delta positive from price now to previous price, if so it went down.
            sumdn = sumdn + (price_list[-i] - price_list[-i+1]) # Sum up all of the down moves in a way that generates a positive sum.
            # DEBUG print(-i,-i+1,price_list[-i],price_list[-i+1],sumdn)
        else:
            sumup = sumup + (price_list[-i+1] - price_list[-i]) # Sum up all of the positive moves in a way that generates a positive sum.
            # DEBUG print("                                       ",-i,-i+1,price_list[-i],price_list[-i+1],sumup)


    rsi = 100 - (100 /(1 + (sumup/(sumdn+0.000001)))) # Prevent div by zero

    return rsi



def persistance(data,lookback=10):
    ''' Test for the persistance of a recent price trend. Mostly a momentum test to validate a solid price move before transacting.'''
    trend = 0
    # Backwards, but this means walking forward from 10 back through the list.
    for n in range(10,1,-1):

        # Always wait 1 time unit before testing.
        if len(data) > 10:
                        if data[-(n+1)] < data[-n]:
                                trend += 1
                        elif data[-(n+1)] > data[-n]:
                                trend -= 1
        else:
            print("Data Too Short to do persistance!")


    return trend



def eff_ratio(data,lookback=240):
        ''' Efficency Ratio: Works like looking at the fractal coastline distance. The numerator takes a big yardstick across all the data
            the denominator takes a measure of each step of the data. Then the ratio is obtained. If it is 1 they coincide. Lower values
            report more of a mean reversion or noisy type of movement. '''

        total = 0

        # Calculate the efficency ratio over 30 time periods
        for n in range(-1,-lookback,-1):
                total += abs(data[n]-data[n-1])

        # Protect against div/0
        if total > 0:
                eff_ratio = abs(data[-lookback]-data[-1])/total
        else:
                eff_ratio = 0

        return eff_ratio


def ema_calculate(list,ema_time_constant=20):
        ''' Calculate the ema in a simple way that uses nothing fancy, so it will run on any PC or server 
        including the R-pi and hosted servers that don't allow Python packages to be installed by a user 
        k = 2 / (Period + 1) where period is the ema_time_constant. The MACD technically uses 3 EMA's
        an EMA 12 and EMA 26 and an EMA 9 of the difference.
         an EMA 12 and EMA 26 and an EMA 9 of the difference.
         EMA=Price(t)k+EMA(y)(1k)
         where:t=today
         y=yesterday
         N=number of days in EMA
         k=2(N+1)'''


        #Calculate k for the ema_time_constant
        k = 2 / (ema_time_constant + 1.0)

        # Slice out a sublist to do the ema on, of length of ema_time_constant.
        sub_list = list[-ema_time_constant:]
        old_ema = sub_list[0]

        for i in range(0,ema_time_constant):
                ema = k * sub_list[i] + (1-k) * old_ema
                #print(i,sub_list[i],ema)
                old_ema=ema

        return ema


#http://www.i-programmer.info/programming/python/3942-arrays-in-python.html
#https://stackoverflow.com/questions/13728392/moving-average-or-running-mean
# Moving Average Function for temps


def simple_mov_avg(mylist,N = 10):

        cumsum, moving_aves = [0], []
                # Put this in because it will fail without it occasionally.
        moving_ave = 0

        for i, x in enumerate(mylist, 1):
                cumsum.append(cumsum[i-1] + x)
                if i>=N:
                        moving_ave = (cumsum[i] - cumsum[i-N])/N
                        #can do stuff with moving_ave here
                        moving_aves.append(moving_ave)
        return moving_ave


def sma_calculate(list,n,sma_time_constant=20):

        if n > sma_time_constant:
                sma = simple_mov_avg(list[(n-sma_time_constant):n],sma_time_constant) 
        else:
                sma = float(list[n])
        return sma


def clip_floor(value,floor_val):
    ''' Take in a value and clip it to the rail formed by floor_val and rtn it. '''
    if value < floor_val:
        value = floor_val

    return value    

''' CBPRO RELATED DATA RETREVAL'''



def check_available_assets(check_holds=False):
    ''' Legacy version of this function. Does not take key,secret and passphrase. Only works with the default portfolio on CBPro.
        Originally there was only one portfolio, one set of keys. So this is the code that started out in the beginning. 
        Supports all code that just trades in the default portfolio. '''
    available_dict = {'BCH': '1', 'BTC': '0.00294188', 'ETC': '10', 'ETH': '1', 'LTC': '1', 'USD': '109.448071399213'}

    # Read in the amounts available to see if a trade is possible.
    available_dict = cbpro_read_available()

    if check_holds:
        holds_dict = cbpro_read_holds()
        return available_dict,holds_dict
    else:
        return available_dict
        
def check_available_assets_PATCH(key,b64secret,passphrase,check_holds=False):
    ''' A PATCH for now. Until possible rewrite of the function above and/or the legacy code that uses it. This fxn
        requires the key,secret and passphrase to be passed in, from which it passes them on to the cbpro read avail.
        Which has been modified to take the optional params of key,secret,passphrase. '''

    available_dict = {'BCH': '1', 'BTC': '0.00294188', 'ETC': '10', 'ETH': '1', 'LTC': '1', 'USD': '109.448071399213'}
    
    # Read in the amounts available to see if a trade is possible.
    available_dict = cbpro_read_available(key,b64secret,passphrase)

    if check_holds:
        holds_dict = cbpro_read_holds(key,b64secret,passphrase) # Holding anything in an order ?
        return available_dict,holds_dict
    else:
        return available_dict

def read_lines_from_csv_file(ticker_filename,volume_rtn=False,extended=False):
    ''' This is a version that goes beyond that used in pairs+mrt. Developed for the Ichimoku trader and then the de-mrt traders. 
    Creates a list of dictionaries, versus a bunch of labelled lists used by legacy code. Pairs+mrt and LTCM notably. 
    Can return volume or not return volume based on switch in call. This saves a bit if volume not needed, no fetch of it.
    '''

    #ticker_filename = "/tmp/five-min-all-coins-ticker.csv"
    # Read in the data using the CSV reader.
    with open(ticker_filename) as f:
        reader = csv.reader(f)


        price_dict = { "time stamp":'',"BTC Price":0,"BCH Price":0,"ETC Price":0,"ETH Price":0,"LTC Price":0,"XRP Price":0,"DAI Price":0}
        volume_dict = { "time stamp":'',"BTC Volume":0,"BCH Volume":0,"ETC Volume":0,"ETH Volume":0,"LTC Volume":0,"XRP Volume":0,"DAI Volume":0}



        date_list = []
        price_list = []
        volume_list = []

        # This just iterates through the file to get the last value.        
        for row in reader:
            try:
                    #price_dict["time stamp"] = row[0]
                    #volume_dict["time stamp"] = row[0]
                    price_dict["BTC Price"] = float(row[1])
                    price_dict["BCH Price"] = float(row[2])
                    price_dict["ETC Price"] = float(row[3])
                    price_dict["ETH Price"] = float(row[4])
                    price_dict["LTC Price"] = float(row[5])
                    
                    volume_dict["BTC Volume"] = float(row[6])
                    volume_dict["BCH Volume"] = float(row[7])
                    volume_dict["ETC Volume"] = float(row[8])
                    volume_dict["ETH Volume"] = float(row[9])
                    volume_dict["LTC Volume"] = float(row[10])
                    price_dict["XRP Price"] = float(row[11])
                    volume_dict["XRP Volume"] = float(row[12])
                    price_dict["DAI Price"] = float(row[13])
                    volume_dict["DAI Volume"] = float(row[14])
                    price_dict["XLM Price"] = float(row[15])
                    volume_dict["XLM Volume"] = float(row[16])
                    price_dict["LINK Price"] = float(row[17])
                    volume_dict["LINK Volume"] = float(row[18])
                    price_dict["ALGO Price"] = float(row[19])
                    volume_dict["ALGO Volume"] = float(row[20])
                    price_dict["ATOM Price"] = float(row[21])
                    volume_dict["ATOM Volume"] = float(row[22])                    
                    price_dict["OXT Price"] = float(row[23])
                    volume_dict["OXT Volume"] = float(row[24])
                    # AUG 2020  
                    price_dict["ZEC Price"] = float(row[25])
                    volume_dict["ZEC Volume"] = float(row[26])                          
                    price_dict["BAT Price"] = float(row[27])
                    volume_dict["BAT Volume"] = float(row[28])
                    price_dict["CVC Price"] = float(row[29])
                    volume_dict["CVC Volume"] = float(row[30])
                    price_dict["GNT Price"] = float(row[31])
                    volume_dict["GNT Volume"] = float(row[32])
                    price_dict["MANA Price"] = float(row[33])
                    volume_dict["MANA Volume"] = float(row[34])
                    price_dict["LOOM Price"] = float(row[35])
                    volume_dict["LOOM Volume"] = float(row[36])
                    price_dict["CGLD Price"] = float(row[37])
                    volume_dict["CGLD Volume"] = float(row[38])                    
                    price_dict["KNC Price"] = float(row[39])
                    volume_dict["KNC Volume"] = float(row[40])
                    price_dict["OMG Price"] = float(row[41])
                    volume_dict["OMG Volume"] = float(row[42])
                    price_dict["ZRX Price"] = float(row[43])
                    volume_dict["ZRX Volume"] = float(row[44])
                    # Any new coins that are not in the hourly,daily,weekly dat$
                    if True or extended:        # PATCH
                            price_dict["FIL Price"] = float(row[45])
                            volume_dict["FIL Volume"] = float(row[46])
                            price_dict["NU Price"] = float(row[47])
                            volume_dict["NU Volume"] = float(row[48])


            except ValueError:
                print('missing data')
            else:
                    # Need to use the dict function to append a dictionary except when just adding an element otherwise it just appends a pointer
                    # This pointer then just points at the last item all the time. This is a wierd one took
                    # A while to figure out! But luckily I had to switch to just sticking the outputs into variables after all.
                    price_list.append(dict(price_dict))
                    if volume_rtn:
                        volume_list.append(dict(volume_dict)) # Get volume only if requested.
                    #date_list.append(price_dict["time stamp"])


    # TOP OF PRINTOUT
    print("<P><b> Data List Input File: </b>"+ticker_filename+"</p><b> Number of Lines in Data List File : </b>",len(price_list))
    print("</P>")                    

    # Could volume be used to determine movement/momentum???
    if volume_rtn: # Return volume only if requested
        return price_list,volume_list
    else:
        return price_list



def read_portfolio_size():
    ''' Read in the portfolio amount and return it as a float. '''


    try:
        with open('portfolio_size.json') as f_obj:
            portfolio_size = json.load(f_obj)
    except IOError:
        raise Exception("Missing portfolio_size.json, need to run cbpro_read_accts.py to init and periodically update it !")


    return float(portfolio_size)
        
 

# DATA FETCHING FOR ICHIMOKU
    
def read_ichimoku_state_from_file(filename="ichimoku_state.json"):
    '''  Helper function to read in the top of cloud level values in, along with 
    the hold state, -1 sold, 1 buy and holding, 0 init'd. plus the score based on
    the price with regard to the levels. Declutters the main function. 
    creates the file if it does not exist, so all auto inits.'''      

    ichimoku_state = {'BTC':{'cld_top':0,'hld':0,'score':0,'fup':0,'fdn':0, "buy_p": 0, "gain": 1, "cuml_gain": 1},
       'BCH':{'cld_top':0,'hld':0,'score':0,'fup':0,'fdn':0, "buy_p": 0, "gain": 1, "cuml_gain": 1},
       'ETC':{'cld_top':0,'hld':0,'score':0,'fup':0,'fdn':0, "buy_p": 0, "gain": 1, "cuml_gain": 1},
       'ETH':{'cld_top':0,'hld':0,'score':0,'fup':0,'fdn':0, "buy_p": 0, "gain": 1, "cuml_gain": 1},
       'LTC':{'cld_top':0,'hld':0,'score':0,'fup':0,'fdn':0, "buy_p": 0, "gain": 1, "cuml_gain": 1},
       'XRP':{'cld_top':0,'hld':0,'score':0,'fup':0,'fdn':0, "buy_p": 0, "gain": 1, "cuml_gain": 1} }


    coinlist = ['ALGO','LINK','XLM']

    for n in coinlist:
        ichimoku_state.update({n:{"cld_top": 0, "hld": 0, "score": 9, "fup": 0, "fdn": 0, "buy_p": 0, "gain": 1, "cuml_gain": 1}})

    

    # If the file exists read it in, if not just create it on the first pass through.
    try:
            with open(filename) as f_obj:
                    ichimoku_state = json.load(f_obj)
    except IOError:
            with open(filename, 'w') as f_obj:
                    json.dump(ichimoku_state,f_obj)

    return ichimoku_state




def average_ichimoku_score(currency_list_working,ichimoku_state):
    ''' A helper funtion that gets the average score for screening on buys, buy only ones that are above this threshold. '''
    sum = 0
    
    for n in currency_list_working:
        sum += ichimoku_state[n]['score']

    avg_score = sum/len(currency_list_working)

    return avg_score


def read_transaction_record_from_file(filename="ltcm_trans_record.json",initable=False):
    '''  Helper function to read in the persistance values in, declutters the main function. 
    creates the file if it does not exist, so all auto inits.
    Allow initing only from the buy sell algo for the master LTCM. Others can't init just readonly.'''      


    # If the file exists read it in, if not just create it on the first pass through.
    try:
            with open(filename) as f_obj:
                    transaction_record = json.load(f_obj)
    except IOError:
            if initable:
                transaction_record = {"XLM": 0, "BCH": 0, "LTC": 0, "ETC": 0, "LINK": 0, "ALGO": 0, "BTC": 0, "ETH": 0, "XRP": 0}
                with open(filename, 'w') as f_obj:
                    json.dump(transaction_record,f_obj)
            else:
                raise Exception("Missing Transaction Record file for LTCM hold states!")

    return transaction_record



def write_transaction_record_to_file(transaction_record,transaction_record_cp,filename="ltcm_trans_record.json"):
    '''  Helper function to write in the persistance file, declutters the main algo function. '''      

    # Only write out the file if the list has changed. OK to check using length as buying and selling are mutually exclusive.    
    if transaction_record != transaction_record_cp:
            with open(filename, 'w') as f_obj:
                    json.dump(transaction_record,f_obj)


# API START                    
def read_api_dict_from_file(filename="api_dict.json"):
    '''  Helper function to read in the api dictionary in, declutters the main function. 
    creates the file if it does not exist, so all auto inits but DOES NOT SAVE to empty dict.
    Takes in filename optionally and then returns api_dict, loaded or {} empty if file not exists. '''


    # If the file exists read it in, if not just create it on the first pass through.
    try:
            with open(filename) as f_obj:
                    api_dict = json.load(f_obj)
    except IOError:
            api_dict = {}

    return api_dict

def reconcile_api_dict(api_dict_local,api_dict):
    ''' Takes in api_dict_local and api_dict. Scans api_dict_local and adds items to api_dict. Then returns api_dict.
        This code assumes that there are no doubles, like upstream the code has been blovked from trading the same currencies.'''
    # Reconcile API Dict with api_dict_local
    for key,value in api_dict_local.items():
        print("local_api_dict -> api_dict: ",key,value)
        api_dict[key] = value

    return api_dict    


def write_api_dict_to_file(api_dict,filename="api_dict.json"):
    '''  Helper function to write in the api_dict taken in to file, declutters the main algo function. '''      
    print("Saving API Dict: ",api_dict)

    with open(filename, 'w') as f_obj:
            json.dump(api_dict,f_obj)

# API END

# REPORTING ON HOLD STATES

def report_holding_states(currency,ltcm_hs,ichi_hs):
    ''' Report on the states of the holds of LTCM and Ichimoku as these will determine if trades are made or a lockout is in effect. '''
        # Print out a small summary of what is happening. Is it holding, did it stop out last, sell at profit or un-init'd so no trade since last training.
    if(ltcm_hs == 1):
            print("<h3>LTCM HOLDING ASSET "+currency+"</h3>")
    elif(ltcm_hs == -1):
            print("<h3>LTCM ASSET "+currency+" has last sold for profit</h3>")
    elif(ltcm_hs == -2):
            print("<h3>LTCM ASSET "+currency+" has last stopped out.</h3>")
    else:
            print("<h3>LTCM ASSET "+currency+" has not traded since training the LTCM model.</h3>")
    # Summary for Ichimoku too     
    if(ichi_hs > 0):
            print("<h3>Ichimoku Trader HOLDING ASSET "+currency+" using the timeframe of "+str(ichi_hs)+"</h3>")
    elif(ichi_hs == -1):
            print("<h3>Ichimoku Trader ASSET "+currency+" has last sold or stopped out</h3>")
    elif(ichi_hs == 0):
            print("<h3>Ichimoku Trader ASSET "+currency+" has last had the state cleared to initial 0.</h3>")
    else:
        print("Invalid Ichimoku State")


def swift_ratio(currency_price_list,multipler=1):
    ''' This concept is taken from looking at https://www.lookintobitcoin.com/charts/bitcoin-investor-tool/
        From looking at this chart got the idea to make a ratio to see what the fib is, but settled on 350 avg after seeing the other chart
        https://www.lookintobitcoin.com/charts/golden-ratio-multiplier/

        This chart shows the Fibonacci numbers, chart was created by Phillip Swift.
        So I wanted to have this ratio to see where  it is on the Fib range. It is the ratio of the current price divided by the sma350.
        This will help to get the ratio that will be used by and algo to decide to accum or dist based on the ratio relative to the Fib #.

        For this codebase, decided to name this ratio after Swift who created the charts.
        More info

        https://medium.com/@positivecrypto/the-golden-ratio-multiplier-c2567401e12a

        multiplier is used to scale up or down based on the time tick of day, hourly = x 24 for example to get daily value.
    '''

    current_price = currency_price_list[-1]
    # Cast to int as weekly uses 1/7.
    sma350 = simple_mov_avg(currency_price_list,int(350*multipler))

    # Protect against div/0
    if sma350 > 0:
        return current_price/sma350
    else:
        return 1 # Safe return value in case of div/0.



def logistic_scaler(n,trade_amount,k=0.2,e=4,offset=None):
        ''' Scales a value using the logistic fxn, much like the tractrix. This version works for buys.
            e for the exponent sets the rate of rise, k sets the limiting value that it rises to as n fall$
            zzero. As in it is the limit reached. When used with the Swift Ratio, allows larger amounts to$
            bought as the price declines. Start with a base of 1 at SR 1 and in the cases of k=0.2 and e=4$
            a max of 2x and about 2x at 0.8 level.

                python logistic-fxn-test.py
                k=.2
                exponent=4

                (1.0, ',', 1.0)
                (0.95, ',', 1.1828414068419983)
                (0.9, ',', 1.4017054082467)
                (0.85, ',', 1.6620354740696497)
                (0.8, ',', 1.9685039370078734)
                (0.75, ',', 2.32375189107413)
                (0.7, ',', 2.7266530334015)
                (0.65, ',', 3.1703571605488676)
                (0.6, ',', 3.640776699029126)
                (0.55, ',', 4.11654981668489)
                (0.5, ',', 4.571428571428571)
                ....
                (0.05, ',', 5.999812505859191)


                                                                '''
        if offset is None:
                return trade_amount * (1+k)/(k + n**e)  # Normal, buy scaling.
        else:
                n = offset - n # Inverse Logistic offset up and fliiped to do sell scaling.
                return trade_amount * (1+k)/(k + n**e)  # Normal part for scaling.



def hold_ratio(total_count,running_avg,new_value,count=1):
    ''' Calculate a running average for the holding average price. This is the target to sell out all the holds at.
        Works similar to IIR filter that recursively adds in the new value in a small proportional to the old, EMA calc style. 
        Used in code that keeps a running average of buys and sells to calculate traget sell prices and intermediate values
        for a stream tye of gain calculatins. Currently 6-2020 used in spike detect and fib-acc-dist.
        Optional count is for sales when multiple holds are sold at once.
        Need to round to 10 as this is a Satoshi and if we are trading BTC pairs need to go all the way down to Sat's'''

    # This equation weighs the currenct average and adds the newly bought at price in,  in proportion to the total.
    return round((running_avg * (total_count-count) + new_value * count) * (1.0/total_count),10)



def index_value_get(price_list):
        ''' Take in a list of prices and compute the index value as a basket of assets. '''
        # The index scaler as calculated on 02/01/2021 via the index-scaler.py code
        index_scaler = {'BTC': 1.2948351898809769e-06, 'BCH': 0.00010715265395693321, 'ETC': 0.005779378023337128, 'ETH': 3.303819215012555e-05, 'LTC': 0.0003332689013457398, 'DAI': 0.04345870445256156, 'XLM': 0.1368368305634366, 'LINK': 0.0019502758831010096, 'ALGO': 0.06871860418771174, 'ATOM': 0.005323651386012638, 'OXT': 0.12584156546907443, 'ZEC': 0.000498396916813309, 'BAT': 0.14554708164274333, 'CVC': 0.2871046102971217, 'GNT': 0.2645354981507646, 'MANA': 0.2889746629905236, 'LOOM': 0.6658232904987016, 'CGLD': 0.015614947877303985, 'KNC': 0.03362587847607519, 'OMG': 0.012470818285212602, 'ZRX': 0.06480732296826613, 'FIL': 0.001938890438924079, 'NU': 0.14377731769036117}
        index_value = 0
        for key in index_scaler:
                #print(price_dict[key+" Price"]*new_dict[key]) # Debug
                index_value += price_list[key+" Price"]*index_scaler[key]

        return index_value



# DEBUG TRACING
def d_trace(msg,var):
    ''' A debug tracer can be called with a message and a variable to trace and it will record them to the debug log file. 
        Also prints out the results as it runs.'''
    filename = "debug-trace.log"

    out_list = []
    
    out_list.append(msg)
    out_list.append(var)
    print("---------------------")
    print("----DEBUG TRACE----: ",msg,var)
    print("---------------------")

    # Open the CSV file and output a row using the out_list
    with open(filename, mode='a') as outfile:
        output_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(out_list)
