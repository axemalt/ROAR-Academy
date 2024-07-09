## This is course material for Introduction to Python Scientific Programming
## Example code: key_search_speed.py
## Author: Allen Y. Yang
##
## (c) Copyright 2020-2024. Intelligent Racing Inc. Not permitted for commercial use

import os
import random
import time

Dictionary10 = dict()
Dictionary1000 = dict()
DictionaryTotal = dict()
file_name = "nasdaqlisted.txt"

# Put IO functions in try -- finally 
print('Reading I/O file ... ', end = ' ')
try:
    # Get the script path

    path = os.path.dirname(os.path.abspath(__file__))

    # Open the file for read
    f_handle = open(path+'/'+file_name,"r")
    f_handle.readline()   # The first line is table captions
    # Create three dictionaries of different lengths
    count = 0
    for line in f_handle:
        count += 1
        ticker, info = line.split('|',1)
        if count<=10:
            Dictionary10[ticker] = info
        if count<=1000:
            Dictionary1000[ticker] = info
        DictionaryTotal[ticker] = info

except IOError:
    print('Cannot open the file ' + file_name)
    exit
finally:
    f_handle.close()

print('done')
            
# Create 1M queries to time the performance of three dictionaries
print('Generating 1M random tickers ... ', end = ' ')
trial_total = 1000000
TICKER_LETTER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
search_list = []
for index in range(trial_total):
    new_random_ticker = ''
    for letter_index in range(random.randint(1,5)):
        new_random_ticker = new_random_ticker + (random.choice(TICKER_LETTER))
    
    search_list.append(new_random_ticker)
print('done')

# Test speed for query Dictionary10
begin_time = time.time()
for index in range(trial_total):
    query_result = search_list[index] in Dictionary10
elapsed_time = time.time() - begin_time
print("Searching a size-{0} dictionary 1M times takes: {1}s".format(len(Dictionary10),
    elapsed_time))

# Test speed for query Dictionary10
begin_time = time.time()
for index in range(trial_total):
    query_result = search_list[index] in Dictionary1000
elapsed_time = time.time() - begin_time
print("Searching a size-{0} dictionary 1M times takes: {1}s".format(len(Dictionary1000),
    elapsed_time))

# Test speed for query Dictionary10
begin_time = time.time()
for index in range(trial_total):
    query_result = search_list[index] in DictionaryTotal
elapsed_time = time.time() - begin_time
print("Searching a size-{0} dictionary 1M times takes: {1}s".format(len(DictionaryTotal),
    elapsed_time))
