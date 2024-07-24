#!/bin/bash
CUR_DIR="/home/br-jmoore/simeng-parameter-study/"
cd $CUR_DIR

#echo "My rank no. is $OMPI_COMM_WORLD_RANK"
index= $(( $1 + $ALPS_APP_PE ))

sleep $(($RANDOM % 3)).$(($RANDOM % 1000))
python3 $CUR_DIR/dispatch_simeng.py $ALPS_APP_PE $index
python3 $CUR_DIR/collect_data.py $ALPS_APP_PE "recollect-results.csv" $index

