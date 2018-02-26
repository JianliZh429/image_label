#!/bin/bash

FILE_DIR=$1
OUT_DIR=$2
BATCH_SIZE=$3

count=0
dir_name=1
output=''
for file in ${FILE_DIR}/*; do
   echo ${file}
   if [ $((${count} % ${BATCH_SIZE})) == 0 ]; then
        output=$( printf '%s%d' ${OUT_DIR} ${dir_name} )
        mkdir -p ${output}
        echo ${output}
        cp -a ${file} ${output}
        dir_name=$(( dir_name + 1))
   else
       cp -a ${file} ${output}
   fi
   count=$(( count+1 ))
done

cd ${OUT_DIR}

dir_name=1

for d in ${OUT_DIR}*; do
    echo ${d}
    IFS='/' read -ra f <<< "${d}"
    name=$( printf '%d.tar.gz' ${dir_name} )
    tar cvzf ${name} ${f[${#f[@]}-1]}
    dir_name=$(( dir_name+1 ))
done