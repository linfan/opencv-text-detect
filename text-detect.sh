#!/bin/bash

if [ "${1}" = "" ]; then
    echo 'Usage: ./text-detect.sh <image-path>'
    exit -1
fi

FILE_PATH=${1}
OUT_DIR=`basename ${FILE_PATH%.*}`
IMAGE_FORMAT=${FILE_PATH##*.}

echo "Read image: ${FILE_PATH}"
echo "Write folder: ${OUT_DIR}"

rm -fr ${OUT_DIR}
python3 opencv_text_area_detect.py ${FILE_PATH} ${OUT_DIR}
for part in `ls ${OUT_DIR}/part-*.jpg`; do
    num=${part##*-}
    tesseract ${part} ${OUT_DIR}/result-${num}
    cat ${OUT_DIR}/result-${num}.txt >> ${OUT_DIR}/result.txt
done
echo "---- RESULT ----"
cat ${OUT_DIR}/result.txt
echo "----------------"
cp ${FILE_PATH} ${OUT_DIR}/origin.${IMAGE_FORMAT}
