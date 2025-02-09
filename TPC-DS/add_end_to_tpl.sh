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
