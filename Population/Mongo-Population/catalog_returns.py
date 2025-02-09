# -*- coding: utf-8 -*-
import pymongo
import codecs  # ✅ Needed for fast UTF-8 file reading in Python 2
from datetime import datetime

# Connect to MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['mongodb1']  # Replace with your database name
collection = db['catalog_returns']

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
        'cr_returned_date_sk': infer_data_type(fields[0]),
        'cr_returned_time_sk': infer_data_type(fields[1]),
        'cr_item_sk': infer_data_type(fields[2]),
        'cr_refunded_customer_sk': infer_data_type(fields[3]),
        'cr_refunded_cdemo_sk': infer_data_type(fields[4]),
        'cr_refunded_hdemo_sk': infer_data_type(fields[5]),
        'cr_refunded_addr_sk': infer_data_type(fields[6]),
        'cr_returning_customer_sk': infer_data_type(fields[7]),
        'cr_returning_cdemo_sk': infer_data_type(fields[8]),
        'cr_returning_hdemo_sk': infer_data_type(fields[9]),
        'cr_returning_addr_sk': infer_data_type(fields[10]),
        'cr_call_center_sk': infer_data_type(fields[11]),
        'cr_catalog_page_sk': infer_data_type(fields[12]),
        'cr_ship_mode_sk': infer_data_type(fields[13]),
        'cr_warehouse_sk': infer_data_type(fields[14]),
        'cr_reason_sk': infer_data_type(fields[15]),
        'cr_order_number': infer_data_type(fields[16]),
        'cr_return_quantity': infer_data_type(fields[17]),
        'cr_return_amount': infer_data_type(fields[18]),
        'cr_return_tax': infer_data_type(fields[19]),
        'cr_return_amt_inc_tax': infer_data_type(fields[20]),
        'cr_fee': infer_data_type(fields[21]),
        'cr_return_ship_cost': infer_data_type(fields[22]),
        'cr_refunded_cash': infer_data_type(fields[23]),
        'cr_reversed_charge': infer_data_type(fields[24]),
        'cr_store_credit': infer_data_type(fields[25]),
        'cr_net_loss': infer_data_type(fields[26])
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
                print("Inserted batch {}".format(i // BATCH_SIZE + 1))  # ✅ Log progress

    if batch:
        collection.insert_many(batch)
        print("Inserted final batch")

import_data('tpc-ds/data/catalog_returns.dat')
