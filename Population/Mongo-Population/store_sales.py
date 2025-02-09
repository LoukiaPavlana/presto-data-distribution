# -*- coding: utf-8 -*-
import pymongo
import codecs
from datetime import datetime

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['mongodb1']  # Replace with your database name
collection = db['store_sales']  # Replace with your collection name

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
    if value in ('y', 'n', 'true', 'false'):  # Faster boolean check
        return value in ('y', 'true')
    try:
        return datetime.strptime(value, '%Y-%m-%d')  # Convert to date
    except ValueError:
        return value  # Default to string

def process_line(line):
    """Processes each line and converts data to appropriate types."""
    fields = line.strip().split('|')
    return {
        'ss_sold_date_sk': infer_data_type(fields[0]),
        'ss_sold_time_sk': infer_data_type(fields[1]),
        'ss_item_sk': infer_data_type(fields[2]),
        'ss_customer_sk': infer_data_type(fields[3]),
        'ss_cdemo_sk': infer_data_type(fields[4]),
        'ss_hdemo_sk': infer_data_type(fields[5]),
        'ss_addr_sk': infer_data_type(fields[6]),
        'ss_store_sk': infer_data_type(fields[7]),
        'ss_promo_sk': infer_data_type(fields[8]),
        'ss_ticket_number': infer_data_type(fields[9]),
        'ss_quantity': infer_data_type(fields[10]),
        'ss_wholesale_cost': infer_data_type(fields[11]),
        'ss_list_price': infer_data_type(fields[12]),
        'ss_sales_price': infer_data_type(fields[13]),
        'ss_ext_discount_amt': infer_data_type(fields[14]),
        'ss_ext_sales_price': infer_data_type(fields[15]),
        'ss_ext_wholesale_cost': infer_data_type(fields[16]),
        'ss_ext_list_price': infer_data_type(fields[17]),
        'ss_ext_tax': infer_data_type(fields[18]),
        'ss_coupon_amt': infer_data_type(fields[19]),
        'ss_net_paid': infer_data_type(fields[20]),
        'ss_net_paid_inc_tax': infer_data_type(fields[21]),
        'ss_net_profit': infer_data_type(fields[22])
    }

def import_data(file_path):
    """Fast data import with batch insert and optimized memory usage."""
    batch = []
    line_count = 0
    with codecs.open(file_path, 'r', 'utf-8') as file:
        for line in file:
            batch.append(process_line(line))
            line_count += 1
            if len(batch) >= BATCH_SIZE:
                collection.insert_many(batch)
                batch = []
                print("Inserted batch {} ({} lines processed)".format(line_count // BATCH_SIZE, line_count))

    if batch:
        collection.insert_many(batch)
        print("Inserted final batch ({} lines processed)".format(line_count))

import_data('tpc-ds/data/store_sales.dat')
