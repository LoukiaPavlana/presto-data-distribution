# TPC-DS

## Overview
TPC-DS is a decision support benchmark that models several generally applicable aspects of a decision support system, including queries and data maintenance. The benchmark provides a representative evaluation of performance as a general purpose decision support system.


For the purposes of our project we extracted a large amount of data from the TPC-DS benchmark as follows
## Useful Links :

https://www.tpc.org/tpcds/

https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-DS_v3.2.0.pdf (specification)

### Prerequisits

install bison (if necessary)

```jsx
sudo apt update
sudo apt install bison
```

### Download in remote server :

```jsx
scp -r /path/to/local/directory username@remote-server:/path/to/destination/
```

## Install gcc-9

```jsx
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt update
sudo apt install gcc-9
gcc-9 --version
```

## **Compile & Generate TPCDS Data**

assume tpc-ds benchmark in in the tpc-ds folder create ‘data’ folder to store the tables:

```jsx
cd tpc-ds
mkdir data
```

- Compile TPCDS DATA:
    - Install gcc-9:
        
        ```jsx
        sudo add-apt-repository ppa:ubuntu-toolchain-r/test
        sudo apt update
        sudo apt install gcc-9
        sudo apt-get install build-essential -y
        gcc-9 --version
        ```
        
    - From tpc-ds/**tools** folder, you need to run make in the tools folder:
        
        ```jsx
        make CC=gcc-9 OS=LINUX
        ```
        
- Populate TPCDS DATA:

```jsx
cd ../tpc-ds/tools
./dsdgen -dir ../data/ -sc 10 -verbose
```

### Generate queries

we added definition for _END

from tpc-ds directory run add_end_to_tpl.sh : 

```jsx
#!/bin/bash

TEMPLATE_DIR="query_templates"

for tpl_file in $TEMPLATE_DIR/*.tpl; do
  if [ -f "$tpl_file" ]; then
    if ! grep -q "define _END" "$tpl_file"; then
      echo "define _END = \";\";" | cat - "$tpl_file" > temp && mv temp "$tpl_file"
      echo "Added define _END to $tpl_file"
    else
      echo "_END already defined in $tpl_file"
    fi
  fi
done

```

**from main directory run run_dsgen.sh :**

```jsx
#!/bin/bash

current_directory="$PWD"
cd tpc-ds/tools
mkdir -p ../../queries

touch qlist.lst
for i in $(seq 1 1 99)
do
  echo "query$i.tpl" >> qlist.lst 
  ./dsqgen \
  -DIRECTORY ../query_templates \
  -INPUT qlist.lst \
  -VERBOSE Y \
  -QUALIFY Y \
  -SCALE 1 \
  -DIALECT netezza \
  -OUTPUT_DIR ../../queries

  mv ../../queries/query_0.sql ../../queries/"query$i.sql" 

done
rm qlist.lst
```


**Mapping the  queries to run on presto:**
```jsx
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


```
