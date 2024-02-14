#!/bin/bash
CUR_DIR="/home/br-jmoore/simeng-parameter-study/"
NUM_BATCHES=1
BATCH_SIZE=64

for BATCH_NUM in $( seq 0 $(($NUM_BATCHES-1)) )
do
    echo "ON BATCH NUMBER $(($BATCH_NUM+1)) / $(($NUM_BATCHES))"
    for BATCH_INDEX in $( seq 0 $(($BATCH_SIZE-1)) )
    do
        #echo $BATCH_INDEX
        python3 $CUR_DIR/dispatch_simeng.py $BATCH_INDEX & #> /dev/null &
    done
    wait
    python3 $CUR_DIR/collect_data.py $BATCH_SIZE "aarch64-results.csv"
done

#echo $PWD

echo "FINISHED"
