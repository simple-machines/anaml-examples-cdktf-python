#!/bin/bash
BQ_LOCATION=australia-southeast1
BQ_PROJECT=<YOUR BQ PROJECT>
BQ_DATASET=tpcds_scale_1

bq mk --location=$BQ_LOCATION --project_id $BQ_PROJECT $BQ_DATASET
bq mk --schema ./schemas/dbgen_version.json $BQ_PROJECT:${BQ_DATASET}.dbgen_version
bq mk --schema ./schemas/customer_address.json $BQ_PROJECT:${BQ_DATASET}.customer_address
bq mk --schema ./schemas/customer_demographics.json $BQ_PROJECT:${BQ_DATASET}.customer_demographics
bq mk --schema ./schemas/date_dim.json $BQ_PROJECT:${BQ_DATASET}.date_dim
bq mk --schema ./schemas/warehouse.json $BQ_PROJECT:${BQ_DATASET}.warehouse
bq mk --schema ./schemas/ship_mode.json $BQ_PROJECT:${BQ_DATASET}.ship_mode
bq mk --schema ./schemas/time_dim.json $BQ_PROJECT:${BQ_DATASET}.time_dim
bq mk --schema ./schemas/reason.json $BQ_PROJECT:${BQ_DATASET}.reason
bq mk --schema ./schemas/income_band.json $BQ_PROJECT:${BQ_DATASET}.income_band
bq mk --schema ./schemas/item.json $BQ_PROJECT:${BQ_DATASET}.item
bq mk --schema ./schemas/store.json $BQ_PROJECT:${BQ_DATASET}.store
bq mk --schema ./schemas/call_center.json $BQ_PROJECT:${BQ_DATASET}.call_center
bq mk --schema ./schemas/customer.json $BQ_PROJECT:${BQ_DATASET}.customer
bq mk --schema ./schemas/web_site.json $BQ_PROJECT:${BQ_DATASET}.web_site
bq mk --schema ./schemas/store_returns.json $BQ_PROJECT:${BQ_DATASET}.store_returns
bq mk --schema ./schemas/household_demographics.json $BQ_PROJECT:${BQ_DATASET}.household_demographics
bq mk --schema ./schemas/web_page.json $BQ_PROJECT:${BQ_DATASET}.web_page
bq mk --schema ./schemas/promotion.json $BQ_PROJECT:${BQ_DATASET}.promotion
bq mk --schema ./schemas/catalog_page.json $BQ_PROJECT:${BQ_DATASET}.catalog_page
bq mk --schema ./schemas/inventory.json $BQ_PROJECT:${BQ_DATASET}.inventory
bq mk --schema ./schemas/catalog_returns.json $BQ_PROJECT:${BQ_DATASET}.catalog_returns
bq mk --schema ./schemas/web_returns.json $BQ_PROJECT:${BQ_DATASET}.web_returns
bq mk --schema ./schemas/web_sales.json $BQ_PROJECT:${BQ_DATASET}.web_sales
bq mk --schema ./schemas/catalog_sales.json $BQ_PROJECT:${BQ_DATASET}.catalog_sales
bq mk --schema ./schemas/store_sales.json $BQ_PROJECT:${BQ_DATASET}.store_sales
