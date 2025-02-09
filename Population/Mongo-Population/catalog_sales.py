# -*- coding: utf-8 -*-
import pymongo
import codecs
from datetime import datetime

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['mongodb1']  # Replace with your database name
collection = db['catalog_sales']  # Replace with your collection name

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
        'cs_sold_date_sk': infer_data_type(fields[0]),
        'cs_sold_time_sk': infer_data_type(fields[1]),
        'cs_ship_date_sk': infer_data_type(fields[2]),
        'cs_bill_customer_sk': infer_data_type(fields[3]),
        'cs_bill_cdemo_sk': infer_data_type(fields[4]),
        'cs_bill_hdemo_sk': infer_data_type(fields[5]),
        'cs_bill_addr_sk': infer_data_type(fields[6]),
        'cs_ship_customer_sk': infer_data_type(fields[7]),
        'cs_ship_cdemo_sk': infer_data_type(fields[8]),
        'cs_ship_hdemo_sk': infer_data_type(fields[9]),
        'cs_ship_addr_sk': infer_data_type(fields[10]),
        'cs_call_center_sk': infer_data_type(fields[11]),
        'cs_catalog_page_sk': infer_data_type(fields[12]),
        'cs_ship_mode_sk': infer_data_type(fields[13]),
        'cs_warehouse_sk': infer_data_type(fields[14]),
        'cs_item_sk': infer_data_type(fields[15]),
        'cs_promo_sk': infer_data_type(fields[16]),
        'cs_order_number': infer_data_type(fields[17]),
        'cs_quantity': infer_data_type(fields[18]),
        'cs_wholesale_cost': infer_data_type(fields[19]),
        'cs_list_price': infer_data_type(fields[20]),
        'cs_sales_price': infer_data_type(fields[21]),
        'cs_ext_discount_amt': infer_data_type(fields[22]),
        'cs_ext_sales_price': infer_data_type(fields[23]),
        'cs_ext_wholesale_cost': infer_data_type(fields[24]),
        'cs_ext_list_price': infer_data_type(fields[25]),
        'cs_ext_tax': infer_data_type(fields[26]),
        'cs_coupon_amt': infer_data_type(fields[27]),
        'cs_ext_ship_cost': infer_data_type(fields[28]),
        'cs_net_paid': infer_data_type(fields[29]),
        'cs_net_paid_inc_tax': infer_data_type(fields[30]),
        'cs_net_paid_inc_ship': infer_data_type(fields[31]),
        'cs_net_paid_inc_ship_tax': infer_data_type(fields[32]),
        'cs_net_profit': infer_data_type(fields[33])
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

import_data('tpc-ds/data/catalog_sales.dat')
