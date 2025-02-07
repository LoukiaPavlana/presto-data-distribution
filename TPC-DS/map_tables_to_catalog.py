
import os

# Define table mappings with catalog and database
table_mappings = {
    'store_returns': 'mongodb.mongodb_presto.store_returns',
    'date_dim': 'memory.default.date_dim',
    'store': 'memory.default.store',
    'customer': 'memory.default.customer',
    'web_returns': 'mongodb.mongodb_presto.web_returns',
    'catalog_sales': 'mongodb.mongodb_presto.catalog_sales',
    'catalog_returns': 'mongodb.mongodb_presto.catalog_returns',
    'web_sales': 'mongodb.mongodb_presto.web_sales',
    'store_sales': 'mongodb.mongodb_presto.store_sales',
    'catalog_page': 'mongodb.mongodb_presto.catalog_page',
    'inventory': 'mysql.prestodb.inventory',
    'warehouse': 'mysql.prestodb.warehouse',
    'item': 'mysql.prestodb.item',
    'time_dim': 'memory.default.time_dim',
    'customer_address': 'memory.default.customer_address',
    'household_demographics': 'memory.default.household_demographics',
    'reason': 'memory.default.reason',
    'income_band': 'memory.default.income_band',
    'ship_mode': 'memory.default.ship_mode',
    'call_center': 'memory.default.call_center',
    'promotion': 'memory.default.promotion',
    'web_site': 'memory.default.web_site',
    'customer_demographics': 'memory.default.customer_demographics'
}

# Path to the folder containing queries
queries_folder = 'ready_queries/'

# Function to update the queries
def update_query(query):
    for old_table, new_table in table_mappings.items():
        # Replace the table names but not the column names
        query = query.replace(" {}".format(old_table), " {}".format(new_table))
        query = query.replace("({}".format(old_table), "({}".format(new_table))
        query = query.replace("{}.{}".format(old_table, ""), "{}.{}".format(new_table, ""))
    return query

# Process each SQL file in the folder
for filename in os.listdir(queries_folder):
    if filename.endswith('.sql'):
        filepath = os.path.join(queries_folder, filename)

        with open(filepath, 'r') as file:
            query = file.read()

        updated_query = update_query(query)

        # Write the updated query back to the file (or to a new file)
        with open(filepath, 'w') as file:
            file.write(updated_query)

        print("Updated" + filename)
