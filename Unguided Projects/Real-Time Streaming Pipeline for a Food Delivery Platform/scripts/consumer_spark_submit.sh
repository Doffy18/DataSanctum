#!/bin/bash


# Activate Python environment

source /home/hdoop/food_orders_env/bin/activate


# Set Java for Spark

export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH


# Force Spark to use this Python from virtualenv

export PYSPARK_PYTHON=/home/hdoop/food_orders_env/bin/python
export PYSPARK_DRIVER_PYTHON=/home/hdoop/food_orders_env/bin/python


# Run Spark Submit for Consumer

spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
  /home/hdoop/Downloads/Food/consumers/orders_stream_consumers.py \
  --config /home/hdoop/Downloads/Food/config/orders_stream.yml

