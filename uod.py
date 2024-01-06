#!/usr/bin/python3

#import matplotlib.pyplot as plt
#from matplotlib import style
#import json
from datetime import datetime
#import pprint
#import pygal
#import os
import csv
#import random
import sys

def read_lines_from_csv_file(t):
    ''' This is a version that goes beyond that used in pairs+mrt. Developed for the Ichimoku trader and then the de-mrt traders. 
    Creates a list of dictionaries, versus a bunch of labelled lists used by legacy code. Pairs+mrt and LTCM notably. 
    '''
    if t == 'h':
	    ticker_filename = '/home/erick/www/btc/cbpro_crypto_price_volume_file.csv'
    elif t == 'd' or t == 'x':
	    ticker_filename = '/home/erick/www/btc/cbpro_crypto_price_volume_file_daily.csv'
    elif t == 'w':
	    ticker_filename = '/home/erick/www/btc/cbpro_crypto_price_volume_file_weekly.csv'
    else:
	    Assert("invalid time frame. h = hourly, d = daily, w = weekly are acceptable.")

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
                    price_dict["time stamp"] = row[0]
                    volume_dict["time stamp"] = row[0]
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
                    price_dict["GLM Price"] = float(row[31])
                    volume_dict["GLM Volume"] = float(row[32])
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
                    price_dict["FIL Price"] = float(row[45])
                    volume_dict["FIL Volume"] = float(row[46])
                    price_dict["AVAX Price"] = float(row[47])
                    volume_dict["AVAX Volume"] = float(row[48])
                    # SPRING 2021       
                    price_dict["NMR Price"] = float(row[49])
                    volume_dict["NMR Volume"] = float(row[50])
                    price_dict["UMA Price"] = float(row[51])
                    volume_dict["UMA Volume"] = float(row[52])
                    price_dict["ADA Price"] = float(row[53])
                    volume_dict["ADA Volume"] = float(row[54])
                    price_dict["UNI Price"] = float(row[55])
                    volume_dict["UNI Volume"] = float(row[56])
                    price_dict["EOS Price"] = float(row[57])
                    volume_dict["EOS Volume"] = float(row[58])
                    price_dict["AAVE Price"] = float(row[59])
                    volume_dict["AAVE Volume"] = float(row[60])
                    price_dict["XTZ Price"] = float(row[61])
                    volume_dict["XTZ Volume"] = float(row[62])
                    price_dict["MKR Price"] = float(row[63])
                    volume_dict["MKR Volume"] = float(row[64])
                    price_dict["COMP Price"] = float(row[65])
                    volume_dict["COMP Volume"] = float(row[66])
                    price_dict["YFI Price"] = float(row[67])
                    volume_dict["YFI Volume"] = float(row[68])
                    price_dict["SNX Price"] = float(row[69])
                    volume_dict["SNX Volume"] = float(row[70])
                    price_dict["OGN Price"] = float(row[71])
                    volume_dict["OGN Volume"] = float(row[72])
                    price_dict["LRC Price"] = float(row[73])
                    volume_dict["LRC Volume"] = float(row[74])
                    price_dict["REN Price"] = float(row[75])
                    volume_dict["REN Volume"] = float(row[76])
                    price_dict["BAL Price"] = float(row[77])
                    volume_dict["BAL Volume"] = float(row[78])
                    price_dict["GRT Price"] = float(row[79])
                    volume_dict["GRT Volume"] = float(row[80])
                    price_dict["BNT Price"] = float(row[81])
                    volume_dict["BNT Volume"] = float(row[82])
                    price_dict["NKN Price"] = float(row[83])
                    volume_dict["NKN Volume"] = float(row[84])
                    price_dict["MATIC Price"] = float(row[85])
                    volume_dict["MATIC Volume"] = float(row[86])
                    price_dict["SKL Price"] = float(row[87])
                    volume_dict["SKL Volume"] = float(row[88])
                    price_dict["ANKR Price"] = float(row[89])
                    volume_dict["ANKR Volume"] = float(row[90])
                    price_dict["STORJ Price"] = float(row[91])
                    volume_dict["STORJ Volume"] = float(row[92])
                    #price_dict[" Price"] = float(row[])
                    #volume_dict[" Volume"] = float(row[])
                    price_dict["CRV Price"] = float(row[93])
                    volume_dict["CRV Volume"] = float(row[94])
                    price_dict["MLN Price"] = float(row[95])
                    volume_dict["MLN Volume"] = float(row[96])
                    price_dict["RLC Price"] = float(row[97])
                    volume_dict["RLC Volume"] = float(row[98])
                    price_dict["MIR Price"] = float(row[99])
                    volume_dict["MIR Volume"] = float(row[100])
                    price_dict["AMP Price"] = float(row[101])
                    volume_dict["AMP Volume"] = float(row[102])
                    price_dict["ICP Price"] = float(row[103])
                    volume_dict["ICP Volume"] = float(row[104])
                    price_dict["DOGE Price"] = float(row[105])
                    volume_dict["DOGE Volume"] = float(row[106])
                    price_dict["SOL Price"] = float(row[107])
                    volume_dict["SOL Volume"] = float(row[108])
                    price_dict["AXS Price"] = float(row[109])
                    volume_dict["AXS Volume"] = float(row[110])
                    price_dict["QNT Price"] = float(row[111])
                    volume_dict["QNT Volume"] = float(row[112])
                    price_dict["LPT Price"] = float(row[113])
                    volume_dict["LPT Volume"] = float(row[114])
                    price_dict["FET Price"] = float(row[115])
                    volume_dict["FET Volume"] = float(row[116])
                    price_dict["POLY Price"] = float(row[117])
                    volume_dict["POLY Volume"] = float(row[118])
                    price_dict["BOND Price"] = float(row[119])
                    volume_dict["BOND Volume"] = float(row[120])
                    price_dict["DOT Price"] = float(row[121])
                    volume_dict["DOT Volume"] = float(row[122])
                    price_dict["RLY Price"] = float(row[123])
                    volume_dict["RLY Volume"] = float(row[124])
                    price_dict["REQ Price"] = float(row[125])
                    volume_dict["REQ Volume"] = float(row[126])
                    price_dict["FARM Price"] = float(row[127])
                    volume_dict["FARM Volume"] = float(row[128])
                    price_dict["ACH Price"] = float(row[129])
                    volume_dict["ACH Volume"] = float(row[130])
                    price_dict["PLA Price"] = float(row[131])
                    volume_dict["PLA Volume"] = float(row[132])

            except ValueError:
                print('missing data')
            else:
                    # Need to use the dict function to append a dictionary except when just adding an element otherwise it just appends a pointer
                    # This pointer then just points at the last item all the time. This is a wierd one took
                    # A while to figure out! But luckily I had to switch to just sticking the outputs into variables after all.
                    price_list.append(dict(price_dict))
                    volume_list.append(dict(volume_dict))
                    date_list.append(price_dict["time stamp"])


    # TOP OF PRINTOUT
    print("<b>Time of Report: </b>",str(datetime.now()))
    print("<P><b> Data List Input File: </b>"+ticker_filename+"</p><b> Number of Lines in Data List File : </b>",len(price_list))
    print("</P>")                    

    # Could volume be used to determine movement/momentum???
    return price_list,date_list,volume_list



def xread_lines_from_file_csv(mode_flag):
        ''' Read in from the CSV file that is grabbed by code that interfaces with the CBPRO API. It has a date/timestamp in row 0, prices of the 5
        cryptocurrencies that are available and volumes ( not used in the LTCM code at this time) '''
        # Open the file and grab the last line in the file
        # This file needs to have at least one piece of data in it for this to run.
        # Else errors will occur!


        price_dict = { "time stamp":'',"BTC Price":0,"BCH Price":0,"ETC Price":0,"ETH Price":0,"LTC Price":0}
        volume_dict = { "time stamp":'',"BTC Volume":0,"BCH Volume":0,"ETC Volume":0,"ETH Volume":0,"LTC Volume":0}


        # Try to open the file and read in all of the lines into a lines list.
        # If it fails to open, show an error message.
        # 1,2 local hourly,daily. 3,4 raspberrypi hourly,daily. All else = reference file in the dir.

        if mode_flag["Input File"] == 1:
                filename = '/tmp/btc-price-raw.txt'
        elif mode_flag["Input File"] == 2:
                filename = '/tmp/btc-price-raw-daily.txt'
        elif mode_flag["Input File"] == 3:
                filename = '/home/erick/www/btc/cbpro_crypto_price_volume_file.csv'
        elif mode_flag["Input File"] == 4:
                filename = '/home/erick/www/btc/cbpro_crypto_price_volume_file_daily.csv'
        else:
                raise Exception("TRAP: Bad Mode flag for Input File")





        # Read in the data using the CSV reader.
        with open(filename) as f:
                reader = csv.reader(f)

                # A lot of initializing to null lists.
                btc_price_list = []
                btc_volume_list = []
                bch_price_list = []
                bch_volume_list = []
                etc_price_list = []
                etc_volume_list = []
                eth_price_list = []
                eth_volume_list = []
                ltc_price_list = []
                ltc_volume_list = []
    
                date_list = []
                price_list = []
                volume_list = []

                # This just iterates through the file to get the last value.        
                for row in reader:
                        try:
                                price_dict["time stamp"] = row[0]
                                volume_dict["time stamp"] = row[0]
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

                        except ValueError:
                                print('missing data')
                        else:
                                # Need to use the dict function to append a dictionary except when just adding an element otherwise it just appends a pointer
                                # This pointer then just points at the last item all the time. This is a wierd one took
                                # A while to figure out! But luckily I had to switch to just sticking the outputs into variables after all.
                                price_list.append(dict(price_dict))
                                volume_list.append(dict(volume_dict))

                                # Drop the individual pieces of the dictionary into seperate lists.
                                btc_price_list.append(price_dict["BTC Price"])
                                btc_volume_list.append(volume_dict["BTC Volume"])
                                bch_price_list.append(price_dict["BCH Price"])
                                bch_volume_list.append(volume_dict["BCH Volume"])
                                etc_price_list.append(price_dict["ETC Price"])
                                etc_volume_list.append(volume_dict["ETC Volume"])
                                eth_price_list.append(price_dict["ETH Price"])
                                eth_volume_list.append(volume_dict["ETH Volume"])
                                ltc_price_list.append(price_dict["LTC Price"])
                                ltc_volume_list.append(volume_dict["LTC Volume"])


                                date_list.append(price_dict["time stamp"])

        # Case statement to pick which currency to use from the list of 5 available from cbpro. CURRENCY MODE                                
        if mode_flag["Currency"] == "BTC":
                price_list = btc_price_list
        elif mode_flag["Currency"] == "BCH":
                price_list = bch_price_list
        elif mode_flag["Currency"] == "ETC":
                price_list = etc_price_list
        elif mode_flag["Currency"] == "ETH":
                price_list = eth_price_list
        elif mode_flag["Currency"] == "LTC":
                price_list = ltc_price_list
        else:
                raise Exception("TRAP: Bad Mode Flag, for Currency!!!")

        # Print out a header
        # How many are there?
        # TOP OF PRINTOUT
        print("<b>Time of Report: </b>",datetime.now())
        print("<P><b> Data List Input File: </b>"+filename+"</p><b> Number of Lines in Data List File : </b>",len(price_list))
        print("</P>")

        return price_list,date_list,volume_list                        

  



''' -------------------------- MAIN  -------------------------------------------
 Note the use of the file path. Forward slashes are valid, back slashes in a Win
 OS are not valid chars and using forwards instead is OK.

 The filename can be stored in a variable and used. Good for when user input is 
 required or some dynamic, i.e. date and time stamped output to a file is needed.'''
H = []
L = []
O = []
C = []
D = []
V = []
volume_l = []
# Append the real date to the CSV on the right so it is human readable.
final_d_str = []

# Have to append to this list when pulling the list for the currency out of the list of dicts
input_lines = []
# BTC by default
c = 'BTC'
t = 'h'

# Create the offset for the mdates so that the calendar lines up. Start date for data = 8-28-2018

# Calculate the number of days between the two dates
start_date = datetime(1970, 1, 1) # Linux zero day.
end_date = datetime(2018, 8, 28) # The start of the data, from which +1 is added on each loop reading it in.
offset = (end_date - start_date).days + 28  # Calc the offset then add some value that makes it line up, not sure, this might be lost data from Internet drops?

# Map the offset to the date ct which was used since legacy times.
date_ct = offset 


# Text Mode Show, the default for the R-pi
# This is a hack based on some old backtesting code that this code is a fork of.
mode_flag = {"Force Wide Param All Steps": False, "Short List Tune": False, "Pretune": True, "Train Model": True, "HTMLize": True, "Plots": False, "All Plots": False, "Input File": 3, "Step Size Hyper P": 3, "Param File": 2, "Currency": "BTC"}


# Get the currency from the command line. If blank = BTC.
#---------------
# Set default values
currency_default = 'BTC'
timeframe_default = 'h'

# Get the currency and timeframe from the command line. If blank, default to BTC and 'h'.
try:
    script, c, t = sys.argv
except ValueError:
    print("Missing Command Line Args. Defaulting to BTC-USD and 'h'\n")
    currency_label = currency_default
    timeframe_label = timeframe_default
else:
    print("\nCurrency:", c)
    currency_label = c

    print("Timeframe:", t)
    timeframe_label = t






#----------------
price_list,date_lines,volume_list = read_lines_from_csv_file(t)

# Slice out a list from the list of dictionaries using a loop. Might be a better way, not sure.
for line in price_list:
        input_lines.append(line[currency_label+' Price'])

for line in volume_list:
        volume_l.append(line[currency_label+' Volume'])

# DEBUG print(input_lines)

# Format the date from the CBPRO format to just the date, then to an mdate.
d = datetime.strptime(date_lines[0], '%Y-%m-%dT%H:%M:%S.%fZ')
day_string = d.strftime('%Y-%m-%d')

print("Start of Data:",day_string)

testing = len(input_lines) #20000

# How long is the input data, mostly for DEBUG.
print("Lines of input data:",len(input_lines))
# Set date to start of testing position, goto end and move back. Tricky fudge for the fact that matplotlib date conv has issues.
# So instead we take a reference against the first date in the data and move up by the length and set back by our testing data len.
date_ct = int(date_ct + len(input_lines)/24 - testing/24)

# Clip off the data that is going to be plotted.
lines = input_lines[-testing:]
d_lines = date_lines[-testing:]

# Mostly just for DEBUG
print("Lines to process:",len(lines))

# Main loop, move through data in 24 hour steps grabbing the OHLC values and appending the counting date that moves forward.

# Adjust threshold by bricolage to 2 STDDEV, might not work exact as the price has upward bias.
# over the long term.

if t == 'h':
	THRESHOLD = 0.01459 # 0.0156
elif t == 'd':
        THRESHOLD = 0.076
elif t == 'w':
        THRESHOLD = 0.235
elif t == 'x': # EXPERIMENTAL
        THRESHOLD = 0.133
else:
        Assert("Invalid timeframe, h = hourly, d = daily and w = weekly are acceptable.")

dot_ct = 0
for n in range(1,len(lines),1):

        if lines[n] > lines[n-1]*(1+THRESHOLD):
                ch = 'U'
        elif lines[n] < lines[n-1]*(1-THRESHOLD):
                ch = 'D'
        else:
                ch = 'O'
                dot_ct += 1
                #if dot_ct == 23:
                        #print(".", end ="")
                        #dot_ct = 0
        # Appeand the chars for UOD
        H.append(ch)

        # Format the date from the CBPRO format to just the date, getting it into a string format.
        d = datetime.strptime(d_lines[n], '%Y-%m-%dT%H:%M:%S.%fZ')

        # Print out the stats for the last 1000
        if ch != 'O': # and date_ct > len(lines)-1000:
                print(d,"     ",date_ct,lines[n-1], str(lines[n]).ljust(1),ch.ljust(1),str(dot_ct).ljust(1),round(lines[n]/lines[n-1],2))
                dot_ct = 0

        date_ct += 1

''' For Debug
print("------------------------------------------")
print(H)
print("------------------------------------------")
print(L)
print("------------------------------------------")
print(O)
print("------------------------------------------")
print(C)
print("------------------------------------------")
print(D)
#quit()
'''

#print("Today's Date and shift of the date from 1/1/1970: ",day_string,date_ct)

# The header has to be in this format for Ichimoku.py. Can have added fields but, needs these as a minimum.
#,Close,Date,High,Low,Open

# Open a file and write all of the lists to it row by row.
filename = mode_flag['Currency'] + '-uod.txt'

with open(filename, mode='w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


    writer.writerow(H)

output = H
#output = "U,O,D,O,O,O,D,D,O,D,U,O,U,U,U,D,U,U,D,U,D,D,O,D,O,O,D,U,U,D,U,U,U,D,O,U,U,D,O,O,D,O,U,O,D,D,U,O,D,O,O,D,D,O,O,O,U,O,D,O,O,U,D,U,O,D,U,U,D,D,U,U,D,O,U,O,D,D,O"

# Create a dictionary to store the character counts
char_count = {}
x = 0
# Loop through each character in the output
for char in output:
    # Check if the character is already in the dictionary
    if char in char_count:
        # If it is, increment the count for that character
        char_count[char] += 1
    else:
        # If it's not, add the character to the dictionary with a count of 1
        char_count[char] = 1
    x+=1
# Print the character counts
for char, count in char_count.items():
    #print(f"{char}: {count}     {round(count*100/x,1)}%")
    print("{}: {}  {}%".format(char, count,round(count*100/x,1)))

