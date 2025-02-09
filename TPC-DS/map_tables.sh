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
