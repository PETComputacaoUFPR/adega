#! /bin/bash

FILE=$(tail -n +2 "$1") #sem cabeçalho

head -1 $1 #cabeçalho

while read line
do
    ementa=$(echo "$line" | cut -d',' -f15)
   re='^[0-9]+$'
    if  [[ $ementa =~ $re ]] ; then
        echo "$line" | cut -d',' -f1-14 --output-delimiter="," | xargs echo -n
        echo -n ",,"
        echo  "$line" | cut -d',' -f15- --output-delimiter=","
    else
        echo "$line"
    fi
    
done <<< "$FILE"


