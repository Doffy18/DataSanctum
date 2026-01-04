#!/bin/bash
spark-submit \
  --master local[*] \
  --packages org.apache.hudi:hudi-spark3.5-bundle_2.12:1.0.2 \
  --conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
  ../src/etl_competitorsales.py ../config/ecommprod.yml

