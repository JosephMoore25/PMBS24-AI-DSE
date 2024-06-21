#!/bin/bash
CUR_DIR="/home/br-jmoore/simeng-parameter-study/"
cd $CUR_DIR

while true; do
    python3 $CUR_DIR/dispatch_simeng.py $OMPI_COMM_WORLD_RANK
    python3 $CUR_DIR/collect_data.py $OMPI_COMM_WORLD_RANK "aarch64-results.csv"
done

