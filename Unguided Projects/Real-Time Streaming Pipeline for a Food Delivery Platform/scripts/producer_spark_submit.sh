#!/bin/bash
source /home/hdoop/food_orders_env/bin/activate

export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
export PYSPARK_PYTHON=/home/hdoop/food_orders_env/bin/python
export PYSPARK_DRIVER_PYTHON=/home/hdoop/food_orders_env/bin/python

spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.postgresql:postgresql:42.7.3 \
  /home/hdoop/Downloads/Food/producers/orders_cdc_producers1.py \
  --config /home/hdoop/Downloads/Food/config/orders_stream.yml

