
# Real-Time Change Data Capture (CDC) Pipeline with Debezium, Kafka, Spark, and Airflow

## Overview

This project implements a **real-time data pipeline** that captures changes from a **PostgreSQL** database and writes them to **Parquet** files using **Spark Streaming**, orchestrated by **Apache Airflow**. The pipeline leverages **Debezium** and **Kafka** for efficient Change Data Capture (CDC), allowing real-time analytics without traditional batch polling.

---

## Architecture

```text
PostgreSQL --> Debezium --> Kafka --> Spark Streaming --> Parquet
                        ^
                        |
                     Airflow DAGs
```

1. **PostgreSQL**: Source database where transactional changes occur.
2. **Debezium**: Monitors the PostgreSQL WAL (Write-Ahead Log) to capture changes as they happen.
3. **Kafka**: Message broker that decouples the source from downstream consumers.
4. **Spark Streaming**: Consumes Kafka messages and writes them as **Parquet** files for analytics or downstream processing.
5. **Airflow**: Orchestrates the pipeline with DAGs that manage tasks and keep the streaming jobs running continuously.

---

## Why Debezium?

* **Real-Time CDC**: Debezium taps into the database’s WAL rather than querying tables periodically. This ensures **near-zero latency** change capture.
* **Efficiency**: Unlike polling methods (e.g., using Spark directly to read PostgreSQL repeatedly), Debezium avoids heavy database scans and reduces load.
* **Consistency & Ordering**: Captures changes in the exact order they occurred in the database, preserving transactional integrity.

### Debezium vs Traditional Polling

| Feature         | Debezium CDC             | Spark Polling            |
| --------------- | ------------------------ | ------------------------ |
| Latency         | Milliseconds             | Seconds to minutes       |
| Database Load   | Minimal                  | High (full table scans)  |
| Change Ordering | Preserved                | Not guaranteed           |
| Complexity      | Handles schema evolution | Manual handling required |

---

## Why Kafka?

* Acts as a **durable, scalable, and decoupled** messaging layer.
* Supports **multiple consumers**: Spark, other microservices, dashboards, etc.
* Handles **high throughput** with guaranteed delivery semantics.

---

## Why Spark Streaming?

* Consumes **Kafka events** efficiently.
* Applies transformations or aggregations in real-time.
* Writes results to **Parquet**, a highly efficient columnar storage format ideal for analytics and machine learning.

---

## Why Airflow?

* Orchestrates all pipeline tasks with **DAGs (Directed Acyclic Graphs)**.
* Ensures **continuous execution** of streaming pipelines.
* Handles **task retries, logging, and monitoring** automatically.
* Makes managing complex, long-running ETL pipelines simpler and more maintainable.

---

## Features

* Real-time CDC from PostgreSQL.
* Streaming pipeline with **Spark Structured Streaming**.
* Writes data in **Parquet format** for analytics.
* Airflow DAGs for orchestration, retries, and monitoring.
* Scalable and efficient architecture with minimal database load.

---

## Requirements

* PostgreSQL
* Debezium
* Kafka
* Apache Spark (with Spark Streaming)
* Apache Airflow
* Python 3.10+
* Java 8+ (for Kafka and Debezium)

---

## Setup Instructions

1. **Start PostgreSQL** and configure logical replication.
2. **Run Debezium** connector for PostgreSQL.
3. **Start Kafka** kraft.
4. **Configure Spark Streaming** job to consume Kafka events and write to Parquet.
5. **Deploy Airflow DAGs** to orchestrate the pipeline.
6. **Monitor Airflow** UI for DAG execution status.

---

## Usage

* The pipeline runs continuously as long as Airflow DAGs are active.
* You can stop the DAGs to pause streaming, then resume later.
* Parquet files are stored in the configured storage location (local or cloud).

---

## Benefits of this Approach

1. **Real-Time Analytics**: No waiting for batch jobs.
2. **Low Database Impact**: WAL-based CDC is efficient.
3. **Scalable & Fault-Tolerant**: Kafka + Spark can handle large volumes.
4. **Maintainable Pipeline**: Airflow DAGs simplify orchestration and monitoring.

---

## References

* [Debezium Documentation](https://debezium.io/documentation/)
* [Apache Kafka](https://kafka.apache.org/)
* [Spark Structured Streaming](https://spark.apache.org/structured-streaming/)
* [Apache Airflow](https://airflow.apache.org/)

---
