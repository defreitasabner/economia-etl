#!/bin/bash

DOMAINS_DIR="config/domains/"
ENTRYPOINT="cli.py"
TIER="silver"

cd ..
for domain in $(ls $DOMAINS_DIR); do
    echo "Running ETL for domain: $domain"
    for dataset in $(ls $DOMAINS_DIR/$domain); do
        dataset_name=$(basename $dataset .yaml)
        echo "  - Processing dataset: $dataset_name"
        python $ENTRYPOINT --domain $domain --dataset $dataset_name --tier $TIER
    done
done
