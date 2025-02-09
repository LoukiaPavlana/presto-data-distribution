# -*- coding: utf-8 -*-
import pymongo
import codecs
from datetime import datetime

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['mongodb1']  # Replace with your database name
collection = db['web_sales']  # Replace with your collection name

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
        'ws_sold_date_sk': infer_data_type(fields[0]),
        'ws_sold_time_sk': infer_data_type(fields[1]),
        'ws_ship_date_sk': infer_data_type(fields[2]),
        'ws_item_sk': infer_data_type(fields[3]),
        'ws_bill_customer_sk': infer_data_type(fields[4]),
        'ws_bill_cdemo_sk': infer_data_type(fields[5]),
        'ws_bill_hdemo_sk': infer_data_type(fields[6]),
        'ws_bill_addr_sk': infer_data_type(fields[7]),
        'ws_ship_customer_sk': infer_data_type(fields[8]),
        'ws_ship_cdemo_sk': infer_data_type(fields[9]),
        'ws_ship_hdemo_sk': infer_data_type(fields[10]),
        'ws_ship_addr_sk': infer_data_type(fields[11]),
        'ws_web_page_sk': infer_data_type(fields[12]),
        'ws_web_site_sk': infer_data_type(fields[13]),
        'ws_ship_mode_sk': infer_data_type(fields[14]),
        'ws_warehouse_sk': infer_data_type(fields[15]),
        'ws_promo_sk': infer_data_type(fields[16]),
        'ws_order_number': infer_data_type(fields[17]),
        'ws_quantity': infer_data_type(fields[18]),
        'ws_wholesale_cost': infer_data_type(fields[19]),
        'ws_list_price': infer_data_type(fields[20]),
        'ws_sales_price': infer_data_type(fields[21]),
        'ws_ext_discount_amt': infer_data_type(fields[22]),
        'ws_ext_sales_price': infer_data_type(fields[23]),
        'ws_ext_wholesale_cost': infer_data_type(fields[24]),
        'ws_ext_list_price': infer_data_type(fields[25]),
        'ws_ext_tax': infer_data_type(fields[26]),
        'ws_coupon_amt': infer_data_type(fields[27]),
        'ws_ext_ship_cost': infer_data_type(fields[28]),
        'ws_net_paid': infer_data_type(fields[29]),
        'ws_net_paid_inc_tax': infer_data_type(fields[30]),
        'ws_net_paid_inc_ship': infer_data_type(fields[31]),
        'ws_net_paid_inc_ship_tax': infer_data_type(fields[32]),
        'ws_net_profit': infer_data_type(fields[33])
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

import_data('tpc-ds/data/web_sales.dat')
