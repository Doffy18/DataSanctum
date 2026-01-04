import sys
import yaml
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, when, lower, upper, lit, concat_ws, array, expr
from pyspark.sql.types import DoubleType, IntegerType, StringType

def main(config_path):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    input_path_clean = config['sellercatalog']['inputpath_clean']
    input_path_dirty = config['sellercatalog']['inputpath_dirty']
    hudi_output_path = config['sellercatalog']['hudioutputpath']
    quarantine_path = config['sellercatalog']['quarantinepath']

    spark = SparkSession.builder.appName("ETL_SellerCatalog").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    # Read clean and dirty seller catalog CSVs
    df_clean = spark.read.option("header", True).csv(input_path_clean)
    df_dirty = spark.read.option("header", True).csv(input_path_dirty)

    # Union clean and dirty DataFrames
    df_raw = df_clean.unionByName(df_dirty)

    # Basic transformations: trim, case formatting, type casting
    df = df_raw.select(
        trim(col("seller_id")).alias("seller_id"),
        trim(col("item_id")).alias("item_id"),
        trim(col("item_name")).alias("item_name"),
        trim(col("category")).alias("category"),  
        col("marketplace_price").cast(DoubleType()).alias("marketplace_price"),
        col("stock_qty").cast(IntegerType()).alias("stock_qty"),
    )

  

    # Fill null stock_qty with 0
    df = df.fillna({"stock_qty": 0})

    # Data Quality Checks
    cond_seller_id = col("seller_id").isNull()
    cond_item_id = col("item_id").isNull()
    cond_item_name = col("item_name").isNull()
    cond_category = col("category").isNull()
    cond_price = (col("marketplace_price").isNull()) | (col("marketplace_price") <= 0)
    cond_stock = (col("stock_qty").isNull()) | (col("stock_qty") < 0)

    df = df.withColumn("dqfail_reasons_list", array(
        when(cond_seller_id, "missing_seller_id").otherwise(None),
        when(cond_item_id, "missing_item_id").otherwise(None),
        when(cond_item_name, "missing_item_name").otherwise(None),
        when(cond_category, "missing_category").otherwise(None),
        when(cond_price, "invalid_price").otherwise(None),
        when(cond_stock, "invalid_stock").otherwise(None)
    ))

    df = df.withColumn("dqfailure", expr("filter(dqfail_reasons_list, x -> x is not null)"))
    df = df.withColumn("dqfailurereason", concat_ws(";", col("dqfailure")))

    # Debug prints
    total_records = df.count()
    quarantine_records = df.filter(col("dqfailurereason") != "").count()
    clean_records = df.filter(col("dqfailurereason") == "").count()

    print(f"Total records before DQ filter: {total_records}")
    print(f"Records failing DQ (quarantine): {quarantine_records}")
    print(f"Records passing DQ (clean): {clean_records}")

    # Write quarantined records
    df.filter(col("dqfailurereason") != "") \
      .drop("dqfail_reasons_list", "dqfailure", "dqfailurereason") \
      .write.mode("overwrite").option("header", True).csv(quarantine_path)

    # Final clean data
    df_final = df.filter(col("dqfailurereason") == "") \
                 .drop("dqfail_reasons_list", "dqfailure", "dqfailurereason")

    # Hudi write config
    hudi_options = {
        'hoodie.table.name': 'sellercatalog_silver',
        'hoodie.datasource.write.recordkey.field': 'seller_id,item_id',
        'hoodie.datasource.write.precombine.field': 'marketplace_price',
        'hoodie.datasource.write.operation': 'upsert',
        'hoodie.datasource.write.table.type': 'COPY_ON_WRITE',
        'hoodie.datasource.write.hive_style_partitioning': 'true',
        'hoodie.upsert.shuffle.parallelism': 2,
        'hoodie.insert.shuffle.parallelism': 2,
        'hoodie.cleaner.policy': 'KEEP_LATEST_FILE_VERSIONS',
    }

    # Write to Hudi
    df_final.write.format("hudi").options(**hudi_options).mode("overwrite").save(hudi_output_path)

    print("SellerCatalog ETL completed successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: etl_sellercatalog.py <config_path>")
        sys.exit(-1)
    main(sys.argv[1])

