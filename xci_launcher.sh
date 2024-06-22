#!/bin/bash
CUR_DIR="/home/br-jmoore/simeng-parameter-study/"
cd $CUR_DIR

#echo "My rank no. is $OMPI_COMM_WORLD_RANK"
sleep $(($RANDOM % 15)).$(($RANDOM % 1000))
while true; do
    sleep $(($RANDOM % 3)).$(($RANDOM % 100))
    python3 $CUR_DIR/dispatch_simeng.py $ALPS_APP_PE
    python3 $CUR_DIR/collect_data.py $ALPS_APP_PE "aarch64-results.csv"
done

