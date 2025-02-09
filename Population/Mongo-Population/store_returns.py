# -*- coding: utf-8 -*-
import pymongo
import codecs
from datetime import datetime

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['mongodb1']  # Replace with your database name
collection = db['store_returns']  # Replace with your collection name

BATCH_SIZE = 10000

def infer_data_type(value):
    """Efficiently infer the data type of a given value."""
    if not value or value == '':
        return None
    try:
        return int(value)  # Convert to integer
    except ValueError:
        try:
            return float(value)  # Convert to float
        except ValueError:
            pass
    if value in ('y', 'n', 'true', 'false'):  # ✅ Faster boolean check
        return value in ('y', 'true')
    try:
        return datetime.strptime(value, '%Y-%m-%d')  # Convert to date
    except ValueError:
        return value  # Default to string

def process_line(line):
    """Processes each line and converts data to appropriate types."""
    fields = line.strip().split('|')
    return {
        'sr_returned_date_sk': infer_data_type(fields[0]),
        'sr_returned_time_sk': infer_data_type(fields[1]),
        'sr_item_sk': infer_data_type(fields[2]),
        'sr_customer_sk': infer_data_type(fields[3]),
        'sr_cdemo_sk': infer_data_type(fields[4]),
        'sr_hdemo_sk': infer_data_type(fields[5]),
        'sr_addr_sk': infer_data_type(fields[6]),
        'sr_store_sk': infer_data_type(fields[7]),
        'sr_reason_sk': infer_data_type(fields[8]),
        'sr_ticket_number': infer_data_type(fields[9]),
        'sr_return_quantity': infer_data_type(fields[10]),
        'sr_return_amt': infer_data_type(fields[11]),
        'sr_return_tax': infer_data_type(fields[12]),
        'sr_return_amt_inc_tax': infer_data_type(fields[13]),
        'sr_fee': infer_data_type(fields[14]),
        'sr_return_ship_cost': infer_data_type(fields[15]),
        'sr_refunded_cash': infer_data_type(fields[16]),
        'sr_reversed_charge': infer_data_type(fields[17]),
        'sr_store_credit': infer_data_type(fields[18]),
        'sr_net_loss': infer_data_type(fields[19])
    }

def import_data(file_path):
    """Fast data import with batch insert."""
    batch = []
    with codecs.open(file_path, 'r', 'utf-8') as file:
        for i, line in enumerate(file):
            batch.append(process_line(line))
            if len(batch) >= BATCH_SIZE:
                collection.insert_many(batch)
                batch = []
                print("Inserted batch {}".format(i // BATCH_SIZE + 1))

    if batch:
        collection.insert_many(batch)
        print("Inserted final batch")

import_data('tpc-ds/data/store_returns.dat')
