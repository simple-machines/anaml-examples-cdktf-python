#!/usr/bin/env python
import os
from constructs import Construct
from cdktf import App, TerraformStack
from imports.anaml.entity import Entity
from imports.anaml.feature import Feature
from imports.anaml.feature_set import FeatureSet
from imports.anaml.table import Table, TableSource, TableEvent
from imports.anaml.provider import AnamlProvider
from imports.anaml_operations.provider import AnamlOperationsProvider
from imports.anaml_operations.data_anaml_operations_source import DataAnamlOperationsSource

class TPCDSStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # Setup the providers
        AnamlProvider(self, "anaml", host=os.environ.get("ANAML_URL"), username=os.environ.get("ANAML_APIKEY"), password=os.environ.get("ANAML_SECRET"), branch="cdktf_tpcds")
        AnamlOperationsProvider(self, "anaml-operations", host=os.environ.get("ANAML_URL"), username=os.environ.get("ANAML_APIKEY"), password=os.environ.get("ANAML_SECRET"))

        # Get the Source as a Data Construct (assumes the source already exists)
        tpcds_source = DataAnamlOperationsSource(self, "tpcds_source", name="tpcds_scale_1") 

        # Setup Entity
        tpcds_customer_entity = Entity(self, id_="tpcds_customer_entity", name="tpcds_customer", description="tpcds customer", default_column="tpcds_customer")

        # Setup Tables
        date_dim = Table(self, "tpcds_date_dim", name="tpcds_date_dim", description="TPCDS date_dim table", source=TableSource(source=tpcds_source.id, table_name="date_dim"))
        customer_raw = Table(self, "tpcds_customer_raw", name="tpcds_customer_raw", description="TPCDS customer table", source=TableSource(source=tpcds_source.id, table_name="customer"))
        household_demographics_raw = Table(self, "household_demographics_raw", name="tpcds_household_demographics", description="TPCDS Customers table", source=TableSource(source=tpcds_source.id, table_name="household_demographics"))
        catalog_sales_raw = Table(self, "tpcds_catalog_sales_raw", name="tpcds_catalog_sales_raw", description="TPCDS catalog_sales table", source=TableSource(source=tpcds_source.id, table_name="catalog_sales"))
        store_sales_raw = Table(self, "tpcds_store_sales_raw", name="tpcds_store_sales_raw", description="TPCDS store_sales table", source=TableSource(source=tpcds_source.id, table_name="store_sales"))
        
        # Setup View Tables
        customer = Table(self,
                    "tpcds_customer",
                    name="tpcds_customer",
                    description="TPCDS customer table joined with dates and demographics",sources=[customer_raw.id, date_dim.id, household_demographics_raw.id],
                    expression="""SELECT dd.d_date as c_last_review_date_date, c.*, h.*
                                FROM tpcds_customer_raw c 
                                INNER JOIN tpcds_date_dim dd ON c.c_last_review_date = dd.d_date_sk
                                INNER JOIN tpcds_household_demographics h ON c.c_current_hdemo_sk = hd_demo_sk""",
                    event=TableEvent(entities={tpcds_customer_entity.id: 'c_customer_sk'}, timestamp_column="c_last_review_date_date"))
        catalog_sales = Table(self,
                    "tpcds_catalog_sales",
                    name="tpcds_catalog_sales",
                    description="TPCDS catalog_sales table joined with dates",sources=[catalog_sales_raw.id, date_dim.id],
                    expression="""SELECT dd.d_date as cs_sold_date_date, cs.*
                                FROM tpcds_catalog_sales_raw cs
                                INNER JOIN tpcds_date_dim dd ON cs.cs_sold_date_sk = dd.d_date_sk
                                """,
                    event=TableEvent(entities={tpcds_customer_entity.id: 'cs_bill_customer_sk'}, timestamp_column="cs_sold_date_date"))
        store_sales = Table(self,
                    "tpcds_store_sales",
                    name="tpcds_store_sales",
                    description="TPCDS store_sales table joined with dates",sources=[store_sales_raw.id, date_dim.id],
                    expression="""SELECT dd.d_date as ss_sold_date_date, ss.*
                                FROM tpcds_store_sales_raw ss
                                INNER JOIN tpcds_date_dim dd ON ss.ss_sold_date_sk = dd.d_date_sk
                                """,
                    event=TableEvent(entities={tpcds_customer_entity.id: 'ss_customer_sk'}, timestamp_column="ss_sold_date_date"))


        core_features = []
        extra_features = []

        # Setup Features
        tpcds_customer_age = Feature(self,
            id_="tpcds_customer_age",
            name="tpcds_customer_age",
            description="Customer age",
            aggregation="last",
            table=customer.id,
            select="datediff(feature_date(), make_date('c_birth_year', 'c_birth_month', 'c_birth_day')) / 365.2425")
        core_features.append(tpcds_customer_age)

        tpcds_preferred_customer = Feature(self,
            id_="tpcds_preferred_customer",
            name="tpcds_preferred_customer",
            description="Preferred Customer",
            aggregation="last",
            table=customer.id,
            select="c_preferred_cust_flag == 'Y'")
        core_features.append(tpcds_preferred_customer)

        tpcds_household_buy_potential = Feature(self,
            id_="tpcds_household_buy_potential",
            name="tpcds_household_buy_potential",
            description="Household Buy Potential",
            aggregation="last",
            table=customer.id,
            select="hd_buy_potential")
        core_features.append(tpcds_household_buy_potential)

        tpcds_household_dependants_count = Feature(self,
            id_="tpcds_household_dependants_count",
            name="tpcds_household_dependants_count",
            description="Household Dependants Count",
            aggregation="last",
            table=customer.id,
            select="hd_dep_count")
        core_features.append(tpcds_household_dependants_count)

        tpcds_customer_has_email = Feature(self,
            id_="tpcds_customer_has_email",
            name="tpcds_customer_has_email",
            description="Customer Has Email Address",
            aggregation="last",
            table=customer.id,
            select="c_email_address is not null")
        extra_features.append(tpcds_customer_has_email)

        self.create_purchase_features(catalog_sales, "catalog", "cs", "order_number", tpcds_customer_entity.id, core_features)
        self.create_purchase_features(store_sales, "store", "ss", "ticket_number", tpcds_customer_entity.id, core_features)

        # Setup Feature Sets
        FeatureSet(self, id_="tpcds_core_20", name="tpcds_core_20", description="Core features", entity=tpcds_customer_entity.id, features=[f.id for f in core_features])
        FeatureSet(self, id_="tpcds_ext_40", name="tpcds_ext_40", description="Extended features", entity=tpcds_customer_entity.id, features=[f.id for f in core_features] + [f.id for f in extra_features])

    
    def create_purchase_features(self, table: Table, table_name: str, prefix: str, basket_col: str, entity_id: int, core_features: list):
        tpcds_sales_max_spend_last_28_days = Feature(self,
            id_=f"tpcds_{table_name}_max_spend_last_28_days",
            name=f"tpcds_{table_name}_max_spend_last_28_days",
            description=f"tpcds_{table_name}_max_spend_last_28_days",
            aggregation="basketsum",
            table=table.id,
            select=f"named_struct('key', {prefix}_{basket_col}, 'value', {prefix}_sales_price)",
            post_aggregation="r -> max_basket(r).value")
        core_features.append(tpcds_sales_max_spend_last_28_days)

        tpcds_sales_big_spender_last_28_days = Feature(self,
            id_=f"tpcds_{table_name}_big_spender_last_28_days",
            name=f"tpcds_{table_name}_big_spender_last_28_days",
            description=f"tpcds_{table_name}_big_spender_last_28_days",
            over=[tpcds_sales_max_spend_last_28_days.id],
            select=f"{tpcds_sales_max_spend_last_28_days.name} > 500",
            entity=entity_id)
        core_features.append(tpcds_sales_big_spender_last_28_days)

        for i in [7, 14]:
            tpcds_sales_visits_last_n_days = Feature(self,
                id_=f"tpcds_{table_name}_visits_last_{i}_days",
                name=f"tpcds_{table_name}_visits_last_{i}_days",
                description=f"tpcds_{table_name}_visits_last_{i}_days",
                aggregation="countdistinct",
                table=table.id,
                select=f"{prefix}_{basket_col}",
                days=i)
            core_features.append(tpcds_sales_visits_last_n_days)

            tpcds_sales_sum_sales_last_n_days = Feature(self,
                id_=f"tpcds_{table_name}_sum_sales_last_{i}_days",
                name=f"tpcds_{table_name}_sum_sales_last_{i}_days",
                description=f"tpcds_{table_name}_sum_sales_last_{i}_days",
                aggregation="sum",
                table=table.id,
                select=f"{prefix}_sales_price",
                days=i)
            core_features.append(tpcds_sales_sum_sales_last_n_days)

            tpcds_sales_max_discount_last_n_days = Feature(self,
                id_=f"tpcds_{table_name}_max_discount_last_{i}_days",
                name=f"tpcds_{table_name}_max_discount_last_{i}_days",
                description=f"tpcds_{table_name}_max_discount_last_{i}_days",
                aggregation="max",
                table=table.id,
                select=f"{prefix}_ext_discount_amt",
                days=i)
            core_features.append(tpcds_sales_max_discount_last_n_days)



app = App()
TPCDSStack(app, "terraform")

app.synth()
