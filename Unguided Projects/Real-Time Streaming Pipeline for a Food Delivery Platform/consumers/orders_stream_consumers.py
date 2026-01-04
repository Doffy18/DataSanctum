from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_date
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType, TimestampType
import yaml
import argparse
import sys


# Load configuration from YAML

parser = argparse.ArgumentParser()
parser.add_argument("--config", required=True, help="Path to YAML config file")
args = parser.parse_args()

with open(args.config, "r") as f:
    config = yaml.safe_load(f)

kafka_conf = config["kafka"]
datalake_conf = config["datalake"]
stream_conf = config["streaming"]

KAFKA_BOOTSTRAP_SERVERS = kafka_conf["brokers"]
KAFKA_TOPIC = kafka_conf["topic"]
DATA_PATH = datalake_conf["path"]
CHECKPOINT = stream_conf["checkpoint_location"]


# Spark session

spark = SparkSession.builder \
    .appName("FoodOrdersStreamConsumer") \
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")


# Schema for incoming JSON

schema = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("customer_name", StringType(), True),
    StructField("restaurant_name", StringType(), True),
    StructField("item", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("order_status", StringType(), True),
    StructField("created_at", TimestampType(), True)
])


# Read stream from Kafka

df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()


# Parse JSON value

df_parsed = df_raw.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")


# Data cleaning

df_clean = df_parsed.filter(
    (col("order_id").isNotNull()) & (col("amount") >= 0)
)


# Add date partition column

df_final = df_clean.withColumn("date", to_date(col("created_at")))


# Write stream to Parquet with partitioning

query = df_final.writeStream \
    .format("parquet") \
    .option("path", DATA_PATH) \
    .option("checkpointLocation", CHECKPOINT) \
    .partitionBy("date") \
    .outputMode("append") \
    .start()

query.awaitTermination()

