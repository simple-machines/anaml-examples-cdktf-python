#!/bin/bash
BQ_DATASET=tpcds_scale_1
GCS_PATH=gs://anaml-tpcds/scale-10000-csv

gsutil ls $GCS_PATH | while read gcs_file ; do
    FILE_NAME=$(echo $gcs_file | sed "s#$GCS_PATH/##g")
    TABLE_NAME=$(echo $FILE_NAME | sed -E 's#_[0-9]*_[0-9]*\.dat##g')
    echo "Loading $gcs_file to $BQ_DATASET"
    bq load --source_format=CSV --field_delimiter '|' --ignore_unknown_values $BQ_DATASET.$TABLE_NAME $GCS_PATH/$FILE_NAME
done
