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
