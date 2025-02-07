select  cast(amc as decimal(15,4))/cast(pmc as decimal(15,4)) am_pm_ratio
 from ( select count(*) amc
       from mongodb.mongodb1.web_sales, memory.default.household_demographics , memory.default.time_dim, mongodb.mongodb1.web_page
       where ws_sold_time_sk = memory.default.time_dim.t_time_sk
         and ws_ship_hdemo_sk = memory.default.household_demographics.hd_demo_sk
         and ws_web_page_sk = mongodb.mongodb1.web_page.wp_web_page_sk
         and memory.default.time_dim.t_hour between 6 and 6+1
         and memory.default.household_demographics.hd_dep_count = 8
         and mongodb.mongodb1.web_page.wp_char_count between 5000 and 5200) at,
      ( select count(*) pmc
       from mongodb.mongodb1.web_sales, memory.default.household_demographics , memory.default.time_dim, mongodb.mongodb1.web_page
       where ws_sold_time_sk = memory.default.time_dim.t_time_sk
         and ws_ship_hdemo_sk = memory.default.household_demographics.hd_demo_sk
         and ws_web_page_sk = mongodb.mongodb1.web_page.wp_web_page_sk
         and memory.default.time_dim.t_hour between 14 and 14+1
         and memory.default.household_demographics.hd_dep_count = 8
         and mongodb.mongodb1.web_page.wp_char_count between 5000 and 5200) pt
 order by am_pm_ratio
 limit 100;

;
~
