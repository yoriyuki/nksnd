#/bin/bash
mkdir -p $2
for file in $1/*.* ; do nkf -Ew $file > $2/${file##*/} ; done;
