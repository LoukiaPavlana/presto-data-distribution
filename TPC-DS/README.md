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

**from tpc-ds directory run add_end_to_tpl.sh :**

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


**Mapping the  queries to run on presto by running map_tables.sh:**
```jsx
#!/bin/bash

INPUT_DIR=$1
OUT_DIR=$2

# Check if two arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_directory> <output_directory>"
    exit 1
fi

# Check if input directory exists
if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: Directory '$INPUT_DIR' does not exist."
    exit 1
fi

# Create output directory if it doesn't exist
if [ ! -d "$OUT_DIR" ]; then
    echo "Creating output directory: $OUT_DIR"
    mkdir -p "$OUT_DIR"
fi

# Define table mappings with the corresponding database and catalog
TABLE_MAPPING="store_returns:mongodb.mongodb1
web_returns:mongodb.mongodb1
catalog_sales:mongodb.mongodb1
catalog_returns:mongodb.mongodb1
web_sales:mongodb.mongodb1
store_sales:mongodb.mongodb1
catalog_page:mongodb.mongodb1
web_page:mongodb.mongodb1
date_dim:mysql.prestodb
inventory:mysql.prestodb
warehouse:mysql.prestodb
item:mysql.prestodb
store:memory.default
customer:memory.default
time_dim:memory.default
customer_address:memory.default
household_demographics:memory.default
reason:memory.default
income_band:memory.default
ship_mode:memory.default
call_center:memory.default
promotion:memory.default
web_site:memory.default
customer_demographics:memory.default"

# Process each .sql file in the input directory
for QUERY_FILE in "$INPUT_DIR"/*.sql; do
    if [ -f "$QUERY_FILE" ]; then
        echo "Processing file: $QUERY_FILE"

        # Generate the output file path
        OUTPUT_FILE="$OUT_DIR/$(basename "$QUERY_FILE")"

        # Backup the original query file before processing
        cp "$QUERY_FILE" "$QUERY_FILE.bak"
        echo "Backup created: $QUERY_FILE.bak"

        # Process each mapping and replace the table names
        for mapping in $TABLE_MAPPING; do
            TABLE_OLD=$(echo $mapping | cut -d':' -f1)
            DB=$(echo $mapping | cut -d':' -f2)

            case $DB in
            "mysql.prestodb")
                TABLE_NEW=mysql.prestodb.$TABLE_OLD ;;
            "mongodb.mongodb1")
                TABLE_NEW=mongodb.mongodb1.$TABLE_OLD ;;
            "memory.default")
                TABLE_NEW=memory.default.$TABLE_OLD ;;
            *)
                echo "Unknown database mapping: $DB"; exit 1 ;;
            esac

            echo "Replacing: $TABLE_OLD -> $TABLE_NEW"

            # Use sed to replace the table name in the file, respecting word boundaries
            sed -i "s/\b$TABLE_OLD\b/$TABLE_NEW/g" "$QUERY_FILE"
        done

        # Move the updated file to the output directory
        mv "$QUERY_FILE" "$OUTPUT_FILE"
        echo "Query file updated: $OUTPUT_FILE"
    else
        echo "No .sql files found in the directory."
    fi
done

```
