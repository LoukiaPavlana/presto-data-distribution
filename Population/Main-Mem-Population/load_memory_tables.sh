#!/bin/bash

# Presto CLI path - update if necessary
PRESTO_CLI="./presto"  # Adjust if installed elsewhere

PRESTO_SERVER="http://[2001:648:2ffe:501:cc00:13ff:fe68:a322]:8080"
CATALOG="memory"
SCHEMA="default"

TABLES=(
  "customer_address"
  "household_demographics"
  "reason"
  "income_band"
  "store"
  "ship_mode"
  "call_center"
  "time_dim"
  "customer"
  "promotion"
  "web_site"
  "customer_demographics"
)

for TABLE in "${TABLES[@]}"; do
  echo "🚀 Loading table: $TABLE ..."

  QUERY="CREATE TABLE $CATALOG.$SCHEMA.$TABLE AS SELECT * FROM tpcds.sf10.$TABLE;"

  echo "$QUERY" | $PRESTO_CLI --server $PRESTO_SERVER --catalog $CATALOG --schema $SCHEMA

  echo "✅ Table $TABLE loaded successfully!"
done

echo "🎯 All tables loaded into Presto memory!"
