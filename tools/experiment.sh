#/bin/bash

experiment () {
  python converter.py -n $1 < ../../corpus/10.kkci > ../output/output-$1.txt
  echo $1, `python evaluate.py ../../corpus/10.sent ../output/output-$1.txt`
};
export -f experiment

if ! [ -d ../output ]; then mkdir ../output; fi
cd ../nksnd
( echo 1 && seq $1 $2 $3 ) | parallel -j -1 experiment {} > ../output/summary.csv
exit 0

# @article{Tange2011a,
#   title = {GNU Parallel - The Command-Line Power Tool},
#   author = {O. Tange},
#   address = {Frederiksberg, Denmark},
#   journal = {;login: The USENIX Magazine},
#   month = {Feb},
#   number = {1},
#   volume = {36},
#   url = {http://www.gnu.org/s/parallel},
#   year = {2011},
#   pages = {42-47},
#   doi = {10.5281/zenodo.16303}
# }
