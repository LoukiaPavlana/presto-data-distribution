# -*- coding: utf-8 -*-

import pymongo
import psutil
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

client = pymongo.MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
db = client['mongodb1']
collection = db['web_returns']

def infer_data_type(value):
    if not value or value == '':
        return None
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            pass
    if value.lower() in ['y', 'n', 'true', 'false']:
        return value.lower() in ['y', 'true']
    try:
        return datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        return value

def process_line(line):
    fields = line.strip().split('|')
    fields = [None if field == '' else infer_data_type(field) for field in fields]

    document = {
        'wr_returned_date_sk': fields[0],
        'wr_returned_time_sk': fields[1],
        'wr_item_sk': fields[2],
        'wr_refunded_customer_sk': fields[3],
        'wr_refunded_cdemo_sk': fields[4],
        'wr_refunded_hdemo_sk': fields[5],
        'wr_refunded_addr_sk': fields[6],
        'wr_returning_customer_sk': fields[7],
        'wr_returning_cdemo_sk': fields[8],
        'wr_returning_hdemo_sk': fields[9],
        'wr_returning_addr_sk': fields[10],
        'wr_web_page_sk': fields[11],
        'wr_reason_sk': fields[12],
        'wr_order_number': fields[13],
        'wr_return_quantity': fields[14],
        'wr_return_amt': fields[15],
        'wr_return_tax': fields[16],
        'wr_return_amt_inc_tax': fields[17],
        'wr_fee': fields[18],
        'wr_return_ship_cost': fields[19],
        'wr_refunded_cash': fields[20],
        'wr_reversed_charge': fields[21],
        'wr_account_credit': fields[22],
        'wr_net_loss': fields[23],
    }

    return document
  
# Function to get dynamic batch size based on available memory
def get_dynamic_batch_size():
    available_memory = psutil.virtual_memory().available
    if available_memory < 500 * 1024 * 1024:  # If <500MB free, use smaller batch
        return 1000
    elif available_memory < 1000 * 1024 * 1024:  # If <1GB free, moderate batch
        return 5000
    else:
        return 10000

def import_data(file_path):
    batch = []
    batch_size = get_dynamic_batch_size()
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            batch.append(process_line(line))

            if len(batch) >= batch_size:
                insert_batch(batch)
                batch = []
                print "Inserted batch {}".format(i // batch_size + 1)

    if batch:
        insert_batch(batch)
        print "Inserted final batch"

def insert_batch(batch):
    retries = 3
    for attempt in range(retries):
        try:
            collection.insert_many(batch, ordered=False)
            return
        except pymongo.errors.AutoReconnect as e:
            print "AutoReconnect Error: {}, retrying in 5 seconds (attempt {}/{})...".format(e, attempt+1, retries)
            time.sleep(5)
        except Exception as e:
            print "Insert error: {}".format(e)
            return

def run_import(file_path, num_threads=4):
    executor = ThreadPoolExecutor(max_workers=num_threads)
    executor.submit(import_data, file_path)

run_import('tpc-ds/data/web_returns.dat')
