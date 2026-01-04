from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_json, struct
import yaml
import argparse

# Load configuration from YAML
parser = argparse.ArgumentParser()
parser.add_argument("--config", required=True, help="Path to YAML config file")
args = parser.parse_args()

with open(args.config, "r") as f:
    config = yaml.safe_load(f)

db_conf = config["postgres"]
kafka_conf = config["kafka"]
stream_conf = config["streaming"]

JDBC_URL = db_conf["jdbc_url"]
DB_TABLE = db_conf["table"]
DB_USER = db_conf["user"]
DB_PASSWORD = db_conf["password"]

KAFKA_BOOTSTRAP_SERVERS = kafka_conf["brokers"]
KAFKA_TOPIC = kafka_conf["topic"]

CHECKPOINT = stream_conf["checkpoint_location"]
BATCH_INTERVAL = stream_conf.get("batch_interval", 5)

# Spark session
spark = (
    SparkSession.builder
    .appName("FoodOrdersCDCProducerSpark")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

# Read from Postgres as a streaming source using rate + foreachBatch pattern
# Here: micro-batch loop that queries Postgres each trigger
def read_postgres():
    return (spark.read
            .format("jdbc")
            .option("url", JDBC_URL)
            .option("dbtable", DB_TABLE)
            .option("user", DB_USER)
            .option("password", DB_PASSWORD)
            .option("driver", "org.postgresql.Driver")
            .load())

# Use a dummy rate stream to trigger periodically, then in foreachBatch read Postgres
rate_stream = (spark.readStream
               .format("rate")
               .option("rowsPerSecond", 1)
               .load())

# Maintain last_processed timestamp via checkpointed state (simplest: filter in SQL by max created_at)
from pyspark.sql.functions import max as spark_max

def foreach_batch(batch_df, batch_id):
    # Global temp view of current table
    pg_df = read_postgres()

    # Get last processed timestamp from previous checkpointed output (if exists)
    # For simplicity here: process all rows each time; you can add incremental logic
    df_to_send = pg_df.select(
        col("order_id"),
        col("customer_name"),
        col("restaurant_name"),
        col("item"),
        col("amount").cast("double"),
        col("order_status"),
        col("created_at")
    )

    # Convert to JSON for Kafka "value"
    kafka_df = df_to_send.select(
        to_json(
            struct(
                "order_id",
                "customer_name",
                "restaurant_name",
                "item",
                "amount",
                "order_status",
                "created_at"
            )
        ).alias("value")
    )

    (kafka_df.write
        .format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)
        .option("topic", KAFKA_TOPIC)
        .save())

# Start the stream with foreachBatch
query = (rate_stream.writeStream
         .outputMode("update")
         .trigger(processingTime=f"{BATCH_INTERVAL} seconds")
         .option("checkpointLocation", CHECKPOINT + "/cdc_producer")
         .foreachBatch(foreach_batch)
         .start())

query.awaitTermination()

