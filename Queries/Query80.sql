with ssr as
 (select  s_store_id as store_id,
          sum(ss_ext_sales_price) as sales,
          sum(coalesce(sr_return_amt, 0)) as returns,
          sum(ss_net_profit - coalesce(sr_net_loss, 0)) as profit
  from mongodb.mongodb1.store_sales left outer join mongodb.mongodb1.store_returns on
         (ss_item_sk = sr_item_sk and ss_ticket_number = sr_ticket_number),
     mysql.prestodb.date_dim,
     memory.default.store,
     mysql.prestodb.item,
     memory.default.promotion
 where ss_sold_date_sk = d_date_sk
       and d_date between cast('1998-08-04' as date)
                  and (cast('1998-08-04' as date) +  30 days)
       and ss_store_sk = s_store_sk
       and ss_item_sk = i_item_sk
       and i_current_price > 50
       and ss_promo_sk = p_promo_sk
       and p_channel_tv = 'N'
 group by s_store_id)
 ,
 csr as
 (select  cp_catalog_page_id as catalog_page_id,
          sum(cs_ext_sales_price) as sales,
          sum(coalesce(cr_return_amount, 0)) as returns,
          sum(cs_net_profit - coalesce(cr_net_loss, 0)) as profit
  from mongodb.mongodb1.catalog_sales left outer join mongodb.mongodb1.catalog_returns on
         (cs_item_sk = cr_item_sk and cs_order_number = cr_order_number),
     mysql.prestodb.date_dim,
     mongodb.mongodb1.catalog_page,
     mysql.prestodb.item,
     memory.default.promotion
 where cs_sold_date_sk = d_date_sk
       and d_date between cast('1998-08-04' as date)
                  and (cast('1998-08-04' as date) +  30 days)
        and cs_catalog_page_sk = cp_catalog_page_sk
       and cs_item_sk = i_item_sk
       and i_current_price > 50
       and cs_promo_sk = p_promo_sk
       and p_channel_tv = 'N'
group by cp_catalog_page_id)
 ,
 wsr as
 (select  web_site_id,
          sum(ws_ext_sales_price) as sales,
          sum(coalesce(wr_return_amt, 0)) as returns,
          sum(ws_net_profit - coalesce(wr_net_loss, 0)) as profit
  from mongodb.mongodb1.web_sales left outer join mongodb.mongodb1.web_returns on
         (ws_item_sk = wr_item_sk and ws_order_number = wr_order_number),
     mysql.prestodb.date_dim,
     memory.default.web_site,
     mysql.prestodb.item,
     memory.default.promotion
 where ws_sold_date_sk = d_date_sk
       and d_date between cast('1998-08-04' as date)
                  and (cast('1998-08-04' as date) +  30 days)
        and ws_web_site_sk = web_site_sk
       and ws_item_sk = i_item_sk
       and i_current_price > 50
       and ws_promo_sk = p_promo_sk
       and p_channel_tv = 'N'
group by web_site_id)
  select  channel
        , id
        , sum(sales) as sales
        , sum(returns) as returns
        , sum(profit) as profit
 from
 (select 'memory.default.store channel' as channel
        , 'memory.default.store' || store_id as id
        , sales
        , returns
        , profit
 from   ssr
 union all
 select 'catalog channel' as channel
        , 'mongodb.mongodb1.catalog_page' || catalog_page_id as id
        , sales
        , returns
        , profit
 from  csr
 union all
 select 'web channel' as channel
        , 'memory.default.web_site' || web_site_id as id
        , sales
        , returns
        , profit
 from   wsr
 ) x
 group by rollup (channel, id)
 order by channel
         ,id
 limit 100;

;
          
