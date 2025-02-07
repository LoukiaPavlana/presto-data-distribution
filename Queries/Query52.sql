select  dt.d_year
        ,mysql.prestodb.item.i_brand_id brand_id
        ,mysql.prestodb.item.i_brand brand
        ,sum(ss_ext_sales_price) ext_price
 from mysql.prestodb.date_dim dt
     ,mongodb.mongodb1.store_sales
     ,mysql.prestodb.item
 where dt.d_date_sk = mongodb.mongodb1.store_sales.ss_sold_date_sk
    and mongodb.mongodb1.store_sales.ss_item_sk = mysql.prestodb.item.i_item_sk
    and mysql.prestodb.item.i_manager_id = 1
    and dt.d_moy=12
    and dt.d_year=1998
 group by dt.d_year
        ,mysql.prestodb.item.i_brand
        ,mysql.prestodb.item.i_brand_id
 order by dt.d_year
        ,ext_price desc
        ,brand_id
limit 100 ;

;
