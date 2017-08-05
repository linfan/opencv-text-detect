#!/bin/bash

if [ "${1}" = "" ]; then
    echo 'Usage: ./text-detect.sh <image-path>'
    exit -1
fi
if [ "${2}" != "" ]; then
    OUT_BASE_FOLDER="${2%%/}/"    # remove ending '/' and put another '/'
fi

FILE_PATH=${1}
OUT_FOLDER=${OUT_BASE_FOLDER}`basename ${FILE_PATH%.*}`
IMAGE_FORMAT=${FILE_PATH##*.}

echo "Read image: ${FILE_PATH}"
echo "Write folder: ${OUT_FOLDER}"

rm -fr ${OUT_FOLDER}
python3 text_detect_wrap.py ${FILE_PATH} ${OUT_FOLDER}
for part in `ls ${OUT_FOLDER}/part-*.jpg`; do
    num=${part##*-}
    tesseract ${part} ${OUT_FOLDER}/result-${num} --oem 1 --psm 13
    cat ${OUT_FOLDER}/result-${num}.txt >> ${OUT_FOLDER}/result.txt
done
cat ${OUT_FOLDER}/result.txt | sed -e 's/^[^a-zA-Z0-9]*//' -e 's/[^a-zA-Z0-9]*$//' > ${OUT_FOLDER}/result.trim.txt
echo "---- RESULT ----"
cat ${OUT_FOLDER}/result.trim.txt
echo "----------------"
cp ${FILE_PATH} ${OUT_FOLDER}/origin.${IMAGE_FORMAT}
