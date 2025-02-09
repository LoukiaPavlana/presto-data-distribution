# Main Mem Population

**(Option 1) Create all tables together by running :**

```jsx
./presto-290/load_memory_tables.sh
```

**(Option 2) From presto's cli we run the following script to populate the main memory**

```jsx
CREATE TABLE memory.default.customer_address AS
SELECT * FROM tpcds.sf10.customer_address;

CREATE TABLE memory.default.household_demographics AS
SELECT * FROM tpcds.sf10.household_demographics;

CREATE TABLE memory.default.reason AS
SELECT * FROM tpcds.sf10.reason;

CREATE TABLE memory.default.income_band AS
SELECT * FROM tpcds.sf10.income_band;

CREATE TABLE memory.default.store AS
SELECT * FROM tpcds.sf10.store;

CREATE TABLE memory.default.ship_mode AS
SELECT * FROM tpcds.sf10.ship_mode;

CREATE TABLE memory.default.call_center AS
SELECT * FROM tpcds.sf10.call_center;

CREATE TABLE memory.default.time_dim AS
SELECT * FROM tpcds.sf10.time_dim;

CREATE TABLE memory.default.customer AS
SELECT * FROM tpcds.sf10.customer;

CREATE TABLE memory.default.promotion AS
SELECT * FROM tpcds.sf10.promotion;

CREATE TABLE memory.default.web_site AS
SELECT * FROM tpcds.sf10.web_site;

CREATE TABLE memory.default.customer_demographics AS 
SELECT * FROM tpcds.sf10.customer_demographics;
```
