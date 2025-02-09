import pymongo
from datetime import datetime

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['mongodb1']  # Replace with your database name
collection = db['web_page']  # Replace with your collection name

def infer_data_type(value):
    """
    Infers the data type of a given value.
    """
    if value is None or value == '':
        return None
    # Try to convert to integer
    try:
        return int(value)
    except ValueError:
        pass
    # Try to convert to float
    try:
        return float(value)
    except ValueError:
        pass
    # Try to convert to boolean
    if value.lower() in ['y', 'n', 'true', 'false']:
        return value.lower() in ['y', 'true']
    # Try to convert to date
    try:
        return datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        pass
    # Otherwise return as string
    return value

def process_line(line):
    """
    Processes each line to handle empty fields, trailing `|`, and converts data to appropriate types.
    """
    fields = line.strip().split('|')

    # Convert empty fields to None (MongoDB NULL equivalent)
    fields = [None if field == '' else infer_data_type(field) for field in fields]

    # Create a document (dictionary) from fields
    document = {
        'wp_web_page_sk': fields[0],
        'wp_web_page_id': fields[1],
        'wp_rec_start_date': fields[2],
        'wp_rec_end_date': fields[3],
        'wp_creation_date_sk': fields[4],
        'wp_access_date_sk': fields[5],
        'wp_autogen_flag': fields[6],
        'wp_customer_sk': fields[7],
        'wp_url': fields[8],
        'wp_type': fields[9],
        'wp_char_count': fields[10],
        'wp_link_count': fields[11],
        'wp_image_count': fields[12],
        'wp_max_ad_count': fields[13],
    }
    return document

def import_data(file_path):
    """
    Imports data from a .dat file to MongoDB.
    Each line is processed, and empty fields are handled.
    """
    with open(file_path, 'r') as file:
        for line in file:
            document = process_line(line)
            collection.insert_one(document)

import_data('tpc-ds/data/web_page.dat')
