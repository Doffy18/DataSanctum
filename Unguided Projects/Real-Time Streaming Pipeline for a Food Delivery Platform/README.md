

# 🍔 Real-Time Streaming Pipeline for a Food Delivery Platform

### Spark CDC Producer → Kafka → Spark Structured Streaming → Parquet Data Lake

This project implements an **end-to-end real-time data streaming pipeline** for a food-delivery platform.
It captures new orders from **PostgreSQL using Spark-based CDC**, publishes them to **Kafka**, processes them with **Spark Structured Streaming**, and stores results in a **Parquet-based Data Lake**.

The pipeline is designed for **low-latency ingestion**, **fault tolerance**, and **scalability**, using industry-standard big-data technologies.

---

## 🚀 Architecture Overview

```
               ┌────────────────────────┐
               │   PostgreSQL Database   │
               │  (food_orders table)    │
               └─────────────┬──────────┘
                             │ Spark CDC Polling
                             ▼
                  ┌───────────────────────────┐
                  │ Spark CDC Producer         │
                  │ (rate + foreachBatch)     │
                  └─────────────┬─────────────┘
                                │ JSON Events
                                ▼
                       ┌──────────────────┐
                       │   Kafka Topic     │
                       │     "orders"      │
                       └──────────┬────────┘
                                  │ Streaming Read
                                  ▼
                    ┌──────────────────────────┐
                    │ Spark Structured Streaming│
                    │   (Orders Consumer)       │
                    └──────────────┬───────────┘
                                   │ Parquet Sink
                                   ▼
                ┌────────────────────────────────┐
                │        Data Lake (Parquet)     │
                │  Partitioned by date=YYYY-MM-DD│
                └────────────────────────────────┘
```

---

## 📁 Project Structure

```
Food/
│
├── producers/
│   └── orders_cdc_producers_spark.py
│
├── consumers/
│   └── orders_stream_consumers.py
│
├── scripts/
│   ├── producer_spark_submit.sh
│   └── consumer_spark_submit.sh
│
├── config/
│   └── orders_stream.yml
│
└── DataLake/
    ├── <parquet output>
    └── checkpoint/
```

---

## ⚙️ Technologies Used

| Component     | Technology                        |
| ------------- | --------------------------------- |
| Database      | PostgreSQL                        |
| Messaging     | Apache Kafka (KRaft mode)         |
| Processing    | Apache Spark Structured Streaming |
| Storage       | Parquet Data Lake                 |
| Language      | Python                            |
| Configuration | YAML                              |
| Serialization | JSON                              |
| Runtime       | Java 11, Python 3.x               |

---

## ✨ Key Features

### ✅ Spark-Based CDC Producer

* Uses **Spark Structured Streaming**
* `rate` source + `foreachBatch` for controlled polling
* Periodically reads new records from PostgreSQL
* Publishes events as **JSON** to Kafka

### ✅ Kafka Consumer with Spark

* Reads Kafka stream
* Parses and validates JSON
* Writes clean data to Parquet

### ✅ Data Lake Design

* Partitioned by date (`created_at → YYYY-MM-DD`)
* Optimized for analytical workloads

### ✅ YAML-Driven Configuration

* No hard-coded values
* Easy environment changes

### ✅ Fault Tolerance

* Spark checkpointing for **exactly-once semantics**

---

## 🧩 Configuration (`orders_stream.yml`)

```yaml
postgres:
  jdbc_url: "jdbc:postgresql://localhost:5432/postgres"
  host: "localhost"
  port: 5432
  db: "postgres"
  user: "postgres"
  password: "hdoop"
  table: "food_orders"

kafka:
  brokers: "localhost:9092"
  topic: "orders"

datalake:
  path: "/home/hdoop/Downloads/Food/DataLake"
  format: "parquet"

streaming:
  checkpoint_location: "/home/hdoop/Downloads/Food/DataLake/checkpoint"
  batch_interval: 5
```

---

## 🧪 How to Run the Pipeline

### Step 1 — Start Kafka (KRaft Mode)

```bash
cd /home/hdoop/Downloads/kafka_2.13-4.1.1
```

Set Java:

```bash
export JAVA_HOME=/usr/lib/jvm/java-25-amazon-corretto
export PATH=$JAVA_HOME/bin:$PATH
```

Format storage:

```bash
sudo ./bin/kafka-storage.sh random-uuid

sudo ./bin/kafka-storage.sh format \
  --cluster-id <cluster-id> \
  --config ./config/server.properties
```

Start Kafka:

```bash
sudo ./bin/kafka-server-start.sh ./config/server.properties
```

---

### Step 2 — Create Kafka Topic

```bash
./bin/kafka-topics.sh --create \
  --topic orders \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1
```

---

### Step 3 — Run Spark CDC Producer

```bash
source food_orders_env/bin/activate
cd /home/hdoop/Downloads/Food/scripts
./producer_spark_submit.sh
```

**What it does**

* Triggers micro-batches every `batch_interval` seconds
* Polls PostgreSQL for new orders
* Pushes events to Kafka

---

### Step 4 — Run Spark Streaming Consumer

```bash
source food_orders_env/bin/activate
cd /home/hdoop/Downloads/Food/scripts
./consumer_spark_submit.sh
```

**What it does**

* Reads Kafka stream
* Parses JSON
* Writes partitioned Parquet files

---

## 📂 Output Data Layout

```
DataLake/
│
├── date=2025-01-01/
│   └── part-0000.parquet
│
├── date=2025-01-02/
│   └── part-0001.parquet
│
└── checkpoint/
```

---

## 🧰 Troubleshooting

### Spark cannot find Kafka package

```bash
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1
```

### Producer sends no data

* Check `batch_interval`
* Verify `created_at` column exists
* Remove old checkpoints if schema changed

### Kafka fails to start

* Re-format storage using `--standalone`
* Ensure correct Java version

---

## 🏁 Conclusion

This project demonstrates a **production-style real-time data pipeline** using:

* Spark-based PostgreSQL CDC
* Kafka event streaming
* Spark Structured Streaming
* Parquet Data Lake storage

It avoids external CDC tools and Python producers, relying entirely on **Spark’s native streaming orchestration**.
