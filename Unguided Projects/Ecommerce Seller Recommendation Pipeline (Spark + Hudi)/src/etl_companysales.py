import sys
import yaml
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, to_date, current_date, array, when, concat_ws, expr
from pyspark.sql.types import IntegerType, DoubleType

def main(config_path):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    input_path_clean = config['companysales']['inputpath_clean']
    input_path_dirty = config['companysales']['inputpath_dirty']
    hudi_output_path = config['companysales']['hudioutputpath']
    quarantine_path = config['companysales']['quarantinepath']

    spark = SparkSession.builder.appName("ETL_CompanySales").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    # Read clean and dirty files
    df_clean = spark.read.option("header", True).csv(input_path_clean)
    df_dirty = spark.read.option("header", True).csv(input_path_dirty)
    df_raw = df_clean.unionByName(df_dirty)

    # Trim and cast columns
    df = df_raw.withColumn("item_id", trim(col("item_id"))) \
           .withColumn("units_sold", col("units_sold").cast(IntegerType())) \
           .withColumn("revenue", col("revenue").cast(DoubleType())) \
           .withColumn("sale_date", to_date(col("sale_date"), 'yyyy-MM-dd'))

    df = df.fillna({'units_sold': 0, 'revenue': 0.0})
    df = df.dropDuplicates(["item_id", "sale_date"])

    # Data Quality Checks
    cond_item_id = col("item_id").isNull()
    cond_units_sold = (col("units_sold") < 0) | col("units_sold").isNull()
    cond_revenue = (col("revenue") < 0) | col("revenue").isNull()
    cond_sale_date = (col("sale_date").isNull()) | (col("sale_date") > current_date())

    df = df.withColumn("dqfail_reasons_list", array(
        when(cond_item_id, "missing_item_id").otherwise(None),
        when(cond_units_sold, "invalid_units_sold").otherwise(None),
        when(cond_revenue, "invalid_revenue").otherwise(None),
        when(cond_sale_date, "invalid_sale_date").otherwise(None)
    ))

    df = df.withColumn("dqfailurereason", concat_ws(";", expr("filter(dqfail_reasons_list, x -> x is not null)")))

    # Separate quarantine and clean records
    df_quarantine = df.filter(col("dqfailurereason") != "")
    df_clean_final = df.filter(col("dqfailurereason") == "").drop("dqfail_reasons_list", "dqfailurereason")

    # Write quarantine data
    df_quarantine.drop("dqfail_reasons_list", "dqfailurereason").write.mode("overwrite").option("header", True).csv(quarantine_path)

    hudi_options = {
        'hoodie.table.name': 'companysales_silver',
        'hoodie.datasource.write.recordkey.field': 'item_id,sale_date',
        'hoodie.datasource.write.precombine.field': 'revenue',
        'hoodie.datasource.write.operation': 'upsert',
        'hoodie.datasource.write.table.type': 'COPY_ON_WRITE',
        'hoodie.upsert.shuffle.parallelism': 2,
        'hoodie.insert.shuffle.parallelism': 2,
        'hoodie.cleaner.policy': 'KEEP_LATEST_FILE_VERSIONS',
    }

    df_clean_final.write.format("hudi").options(**hudi_options).mode("overwrite").save(hudi_output_path)

    print("CompanySales ETL completed successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: etl_companysales.py <config_path>")
        sys.exit(-1)
    main(sys.argv[1])

