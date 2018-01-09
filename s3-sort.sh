#!/usr/bin/env bash
LS=$(aws s3 ls | awk '{print $3}')
export AWS_DEFAULT_REGION=us-east-1
echo "starting" > s3list.tmp
getSize()
{
        aws s3 ls $1 --recursive  --summarize | grep "Total Size" | awk '{print $3}'
}
for bucket in $LS; do
        OUT="$(getSize ${bucket} 2>&1 null)";
        if (grep error <<< $OUT ); then
                BUCKET_SIZE=1024
        else
                BUCKET_SIZE=$OUT
        fi
        MB_SIZE=$(( ${BUCKET_SIZE} / 1024 / 1024 ));
        echo $bucket $MB_SIZE "Mb" >> s3list.tmp;
done
echo "Sorting" > s3list.txt
sort -k2 -n s3list.tmp >> s3list.txt
exit 0
