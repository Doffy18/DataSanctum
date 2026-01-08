from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "dbserver.public.events"

import sys
python_path = sys.executable

spark = (
    SparkSession.builder
    .appName("Kafka-To-Parquet")
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem")
    .config("spark.pyspark.python", python_path)
    .config("spark.pyspark.driver.python", python_path)
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

kafka_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)
    .option("subscribe", KAFKA_TOPIC)
    .option("startingOffsets", "earliest")
    .load()
)

#
# Debezium JSON schema 
dschema = StructType([
    StructField("payload", StructType([
        StructField("op", StringType(), True),
        StructField("ts_ms", LongType(), True),
        StructField("after", StructType([
            StructField("id", LongType(), True),
            StructField("event_id", StringType(), True),
            StructField("user_id", StringType(), True),
            StructField("event_type", StringType(), True),
            StructField("product_id", StringType(), True),
            StructField("price", DoubleType(), True),
            StructField("event_time", StringType(), True)  # IMPORTANT FIX
        ]), True)
    ]), True)
])

parsed_df = kafka_df.select(
    from_json(col("value").cast("string"), dschema).alias("data")
)

parquet_df = parsed_df.select(
    col("data.payload.after.id").alias("id"),
    col("data.payload.after.event_id").alias("event_id"),
    col("data.payload.after.user_id").alias("user_id"),
    col("data.payload.after.event_type").alias("event_type"),
    col("data.payload.after.product_id").alias("product_id"),
    col("data.payload.after.price").alias("price"),
    col("data.payload.after.event_time").alias("event_time"),
    col("data.payload.op").alias("cdc_op"),
    col("data.payload.ts_ms").alias("cdc_ts")
).filter(col("cdc_op") != "d")

# Paths
PARQUET_PATH = "/home/hdoop/Downloads/airflow_kafka_hudi_pipeline/DataLake/parquet"
CHECKPOINT_PATH = "/home/hdoop/Downloads/airflow_kafka_hudi_pipeline/DataLake/parquet_checkpoint"

# Write stream to Parquet
query = (
    parquet_df.writeStream
    .format("parquet")
    .option("path", PARQUET_PATH)
    .option("checkpointLocation", CHECKPOINT_PATH)
    .outputMode("append")
    .start()
)
print("Spark streaming query started successfully")
query.awaitTermination()
