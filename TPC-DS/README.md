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

# Directory where the .tpl files are located
TEMPLATE_DIR="query_templates"

# Loop through all .tpl files in the template directory
for tpl_file in $TEMPLATE_DIR/*.tpl; do
  # Check if the file exists
  if [ -f "$tpl_file" ]; then
    # Insert 'define _END = ";";' at the top of the .tpl file if not already present
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
  echo "query$i.tpl" >> qlist.lst # to create each query in a different file, each time write a new template name into the qlist file
  ./dsqgen \
  -DIRECTORY ../query_templates \
  -INPUT qlist.lst \
  -VERBOSE Y \
  -QUALIFY Y \
  -SCALE 1 \
  -DIALECT netezza \
  -OUTPUT_DIR ../../queries

  mv ../../queries/query_0.sql ../../queries/"query$i.sql" # output of dsqgen for 1 query variant/query is query_0.sql regardless of the query template

done
rm qlist.lst
```
