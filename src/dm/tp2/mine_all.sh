#!/bin/bash
# Script for parameter sweeping different itemset methods
#
# Author: Flavio Figueiredo

if [ $# -lt 1 ]; then
    echo 'Usage $0 <out folder>'
    exit 1
fi

OUTF=$1

COLFOLD=$OUTF/collocations/
FSETFOLD=$OUTF/frequent_sets/

mkdir $COLFOLD 
mkdir $FSETFOLD

for input in `seq 0 24`; do
    for sup in 0.01 0.05 0.1 0.5; do
        supfold=$FSETFOLD/$sup
        mkdir $supfold

        java -cp scripts/spmf/:scripts/spmf/spmf.jar dm.main.MineSetsFP \
            data-isets/$input.isets data-isets/$input.vocab $sup > \
            $supfold/$input.fp.out & 
        java -cp scripts/spmf/:scripts/spmf/spmf.jar dm.main.MineSetsCharm \
            data-isets/$input.isets data-isets/$input.vocab $sup > \
            $supfold/$input.charm.out & 
    done
    wait

    python scripts/collocations.py data-parsed/$input.parsed 1 \
        > $OUTF/collocations/$input.out
done
