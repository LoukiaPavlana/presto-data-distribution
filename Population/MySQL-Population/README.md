# MySQL Population

## 1. Create the database and tables

```jsx
CREATE DATABASE prestodb;
USE prestodb;
```
## 2. Create the tables
**warehouse table:** 

```jsx
CREATE TABLE warehouse (
    w_warehouse_sk INT NOT NULL,           
    w_warehouse_id CHAR(16) NOT NULL,       
    w_warehouse_name VARCHAR(20),         
    w_warehouse_sq_ft INT,                  
    w_street_number CHAR(10),               
    w_street_name VARCHAR(60),              
    w_street_type CHAR(15),                 
    w_suite_number CHAR(10),                
    w_city VARCHAR(60),                     
    w_county VARCHAR(30),                   
    w_state CHAR(2),                        
    w_zip CHAR(10),                       
    w_country VARCHAR(20),                 
    w_gmt_offset DECIMAL(5,2),              
    PRIMARY KEY (w_warehouse_sk)          
);
```

**item table:** 

```jsx
CREATE TABLE item (
    i_item_sk INT NOT NULL,                
    i_item_id CHAR(16) NOT NULL,           
    i_rec_start_date DATE,               
    i_rec_end_date DATE,               
    i_item_desc VARCHAR(200),              
    i_current_price DECIMAL(7,2),         
    i_wholesale_cost DECIMAL(7,2),         
    i_brand_id INT,                        
    i_brand VARCHAR(50),                
    i_class_id INT,                      
    i_class VARCHAR(50),                  
    i_category_id INT,               
    i_category VARCHAR(50),              
    i_manufact_id INT,                    
    i_manufact VARCHAR(50),            
    i_size CHAR(20),                   
    i_formulation CHAR(20),           
    i_color CHAR(20),                  
    i_units CHAR(10),                   
    i_container CHAR(10),           
    i_manager_id INT,                  
    i_product_name CHAR(50),               
    PRIMARY KEY (i_item_sk)                
);
```

**date_dim:**

```jsx
CREATE TABLE date_dim (
    d_date_sk INT NOT NULL,                
    d_date_id CHAR(16) NOT NULL,           
    d_date DATE NOT NULL,                  
    d_month_seq INT,                       
    d_week_seq INT,                       
    d_quarter_seq INT,                     
    d_year INT,                            
    d_dow INT,                            
    d_moy INT,                           
    d_dom INT,                            
    d_qoy INT,                            
    d_fy_year INT,                         
    d_fy_quarter_seq INT,                  
    d_fy_week_seq INT,                
    d_day_name CHAR(9),                
    d_quarter_name CHAR(6),                
    d_holiday CHAR(1),                  
    d_weekend CHAR(1),                    
    d_following_holiday CHAR(1),          
    d_first_dom INT,                      
    d_last_dom INT,                        
    d_same_day_ly INT,                   
    d_same_day_lq INT,                     
    d_current_day CHAR(1),                 
    d_current_week CHAR(1),             
    d_current_month CHAR(1),             
    d_current_quarter CHAR(1),          
    d_current_year CHAR(1),            
    PRIMARY KEY (d_date_sk)           
);
```

**inventory table:**

```jsx
CREATE TABLE inventory (
    inv_date_sk INT NOT NULL,               
    inv_item_sk INT NOT NULL,              
    inv_warehouse_sk INT NOT NULL,        
    inv_quantity_on_hand INT,               
    PRIMARY KEY (inv_date_sk, inv_item_sk, inv_warehouse_sk),  
    FOREIGN KEY (inv_date_sk) REFERENCES date_dim(d_date_sk),  
    FOREIGN KEY (inv_item_sk) REFERENCES item(i_item_sk), 
    FOREIGN KEY (inv_warehouse_sk) REFERENCES warehouse(w_warehouse_sk)  
);
```

## 3. Transfer .dat files to to the MySQL server's data directory

- The purpose of copying the file here is typically to make it accessible for MySQL operations like **`LOAD DATA INFILE`**, which requires the file to be within the MySQL server's designated directories.

```jsx
sudo cp tpc-ds/data/inventory.dat /var/lib/mysql-files/
sudo cp tpc-ds/data/warehouse.dat /var/lib/mysql-files/
sudo cp tpc-ds/data/item.dat /var/lib/mysql-files/
sudo cp tpc-ds/data/date_dim.dat /var/lib/mysql-files/
```

### 4. Populate tables

```jsx
USE mysql_1;
```

**date_dim:**

```jsx
LOAD DATA INFILE '/var/lib/mysql-files/date_dim.dat'
REPLACE INTO TABLE date_dim
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(d_date_sk, d_date_id, d_date, d_month_seq, d_week_seq, d_quarter_seq, d_year, d_dow, d_moy, d_dom, d_qoy,
 d_fy_year, d_fy_quarter_seq, d_fy_week_seq, d_day_name, d_quarter_name, d_holiday, d_weekend, d_following_holiday,
 d_first_dom, d_last_dom, d_same_day_ly, d_same_day_lq, d_current_day, d_current_week, d_current_month,
 d_current_quarter, d_current_year);
```

**item:**

```jsx
LOAD DATA INFILE '/var/lib/mysql-files/item.dat'
INTO TABLE item
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@i_item_sk, @i_item_id, @i_rec_start_date, @i_rec_end_date, @i_item_desc, @i_current_price, @i_wholesale_cost,
 @i_brand_id, @i_brand, @i_class_id, @i_class, @i_category_id, @i_category, @i_manufact_id, @i_manufact, @i_size,
 @i_formulation, @i_color, @i_units, @i_container, @i_manager_id, @i_product_name)
SET
    i_item_sk = @i_item_sk,
    i_item_id = @i_item_id,
    i_rec_start_date = IF(@i_rec_start_date = '', NULL, @i_rec_start_date),
    i_rec_end_date = IF(@i_rec_end_date = '', NULL, @i_rec_end_date),
    i_item_desc = IF(@i_item_desc = '', NULL, @i_item_desc),
    i_current_price = IF(@i_current_price = '', NULL, @i_current_price),
    i_wholesale_cost = IF(@i_wholesale_cost = '', NULL, @i_wholesale_cost),
    i_brand_id = IF(@i_brand_id = '', NULL, @i_brand_id),
    i_brand = IF(@i_brand = '', NULL, @i_brand),
    i_class_id = IF(@i_class_id = '', NULL, @i_class_id),
    i_class = IF(@i_class = '', NULL, @i_class),
    i_category_id = IF(@i_category_id = '', NULL, @i_category_id),
    i_category = IF(@i_category = '', NULL, @i_category),
    i_manufact_id = IF(@i_manufact_id = '', NULL, @i_manufact_id),
    i_manufact = IF(@i_manufact = '', NULL, @i_manufact),
    i_size = IF(@i_size = '', NULL, @i_size),
    i_formulation = IF(@i_formulation = '', NULL, @i_formulation),
    i_color = IF(@i_color = '', NULL, @i_color),
    i_units = IF(@i_units = '', NULL, @i_units),
    i_container = IF(@i_container = '', NULL, @i_container),
    i_manager_id = IF(@i_manager_id = '', NULL, @i_manager_id),
    i_product_name = IF(@i_product_name = '', NULL, @i_product_name);
```

**warehouse:** 

```jsx
LOAD DATA INFILE '/var/lib/mysql-files/warehouse.dat'
INTO TABLE warehouse
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@w_warehouse_sk, @w_warehouse_id, @w_warehouse_name, @w_warehouse_sq_ft, @w_street_number, @w_street_name, @w_street_type,
 @w_suite_number, @w_city, @w_county, @w_state, @w_zip, @w_country, @w_gmt_offset)
SET
    w_warehouse_sk = IF(@w_warehouse_sk = '', NULL, @w_warehouse_sk),
    w_warehouse_id = IF(@w_warehouse_id = '', NULL, @w_warehouse_id),
    w_warehouse_name = IF(@w_warehouse_name = '', NULL, @w_warehouse_name),
    w_warehouse_sq_ft = IF(@w_warehouse_sq_ft = '', NULL, @w_warehouse_sq_ft),
    w_street_number = IF(@w_street_number = '', NULL, @w_street_number),
    w_street_name = IF(@w_street_name = '', NULL, @w_street_name),
    w_street_type = IF(@w_street_type = '', NULL, @w_street_type),
    w_suite_number = IF(@w_suite_number = '', NULL, @w_suite_number),
    w_city = IF(@w_city = '', NULL, @w_city),
    w_county = IF(@w_county = '', NULL, @w_county),
    w_state = IF(@w_state = '', NULL, @w_state),
    w_zip = IF(@w_zip = '', NULL, @w_zip),
    w_country = IF(@w_country = '', NULL, @w_country),
    w_gmt_offset = IF(@w_gmt_offset = '', NULL, @w_gmt_offset);

```

**inventory:**
```jsx
LOAD DATA INFILE '/var/lib/mysql-files/inventory.dat'
INTO TABLE inventory
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@inv_date_sk, @inv_item_sk, @inv_warehouse_sk, @inv_quantity_on_hand)
SET
    inv_date_sk = @inv_date_sk,
    inv_item_sk = @inv_item_sk,
    inv_warehouse_sk = @inv_warehouse_sk,
    inv_quantity_on_hand = IF(@inv_quantity_on_hand = '', NULL, @inv_quantity_on_hand);
```
