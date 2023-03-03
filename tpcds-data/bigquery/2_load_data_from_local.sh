#!/bin/bash
BQ_PROJECT=<YOUR BQ PROJECT>
BQ_DATASET=tpcds_scale_1
LOCAL_PATH=tpcds-scale-1

ls -1 $LOCAL_PATH | while read file ; do
    FILE_NAME=$file
    TABLE_NAME=$(echo $FILE_NAME | sed -E 's#_[0-9]*_[0-9]*\.dat##g')
    echo "Loading $file to $BQ_DATASET"
    bq --project_id $BQ_PROJECT load --source_format=CSV --field_delimiter '|' --ignore_unknown_values $BQ_DATASET.$TABLE_NAME $LOCAL_PATH/$FILE_NAME
done
