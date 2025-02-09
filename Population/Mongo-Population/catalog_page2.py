# -*- coding: utf-8 -*-
import pymongo
import codecs  # ✅ Needed for fast UTF-8 file reading in Python 2
from datetime import datetime

# Connect to MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['mongodb1']  # Replace with your database name
collection = db['catalog_page']  # Replace with your collection name

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
    if value.lower() in ('y', 'n', 'true', 'false'):
        return value.lower() in ('y', 'true')  # Convert to boolean
    try:
        return datetime.strptime(value, '%Y-%m-%d')  # Convert to date
    except ValueError:
        return value  # Default to string

def process_line(line):
    """Processes each line and converts data to appropriate types."""
    fields = [infer_data_type(field) for field in line.strip().split('|')]

    return {
        'cp_catalog_page_sk': fields[0],
        'cp_catalog_page_id': fields[1],
        'cp_start_date_sk': fields[2],
        'cp_end_date_sk': fields[3],
        'cp_department': fields[4],
        'cp_catalog_number': fields[5],
        'cp_catalog_page_number': fields[6],
        'cp_description': fields[7],
        'cp_type': fields[8]
    }

def import_data(file_path):
    """Fast data import with batch insert."""
    batch = []
    with codecs.open(file_path, 'r', 'utf-8') as file:
        for line in file:
            batch.append(process_line(line))
            if len(batch) >= BATCH_SIZE:
                collection.insert_many(batch)
                batch = []

    if batch:
        collection.insert_many(batch)

import_data('tpc-ds/data/catalog_page.dat')
