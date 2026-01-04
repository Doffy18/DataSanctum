
# 🛒 Ecommerce Seller Recommendation Pipeline (Spark + Hudi)

This project builds a **data engineering pipeline** that analyzes internal sales data and competitor sales data to recommend **high-performing products** that sellers currently do not have in their catalog.

The goal is to help sellers **expand their catalog strategically** by identifying top-selling items and estimating their potential revenue impact.

The pipeline focuses on **data quality, incremental processing, and scalable analytics** using Apache Spark and Apache Hudi.

---

## 🚀 High-Level Overview

The system ingests multiple datasets, cleans and validates them, handles schema evolution, and produces seller-level product recommendations.

**Key ideas**

* Medallion architecture (Raw → Processed → Consumption)
* Quarantine zone for bad data
* Incremental, idempotent writes using Hudi
* Business-ready recommendation output

---

## 🏗 Architecture Flow

```
Raw Data (CSV / JSON)
   │
   ▼
ETL Pipelines (Spark)
   ├── Seller Catalog ETL
   ├── Company Sales ETL
   └── Competitor Sales ETL
   │
   ▼
Processed Layer (Apache Hudi Tables)
   │
   ▼
Consumption Layer
   ├── Aggregations
   ├── Missing Item Detection
   └── Revenue Estimation
   │
   ▼
Final Recommendations (CSV)
```

---

## 📁 Project Structure

```
ecommerce_seller_recommendation/
│
├── configs/
│   └── ecomm_prod.yml
│
├── src/
│   ├── etl_seller_catalog.py
│   ├── etl_company_sales.py
│   ├── etl_competitor_sales.py
│   └── consumption_recommendation.py
│
├── scripts/
│   ├── etl_seller_catalog_spark_submit.sh
│   ├── etl_company_sales_spark_submit.sh
│   ├── etl_competitor_sales_spark_submit.sh
│   └── consumption_recommendation_spark_submit.sh
│
└── README.md
```

---

## ⚙️ Tech Stack

| Layer         | Technology                  |
| ------------- | --------------------------- |
| Processing    | Apache Spark (PySpark)      |
| Storage       | Apache Hudi                 |
| Data Format   | CSV, Parquet                |
| Configuration | YAML                        |
| Language      | Python                      |
| Architecture  | Medallion + Quarantine Zone |

---

## 🧹 Data Processing Highlights

### 1️⃣ Seller Catalog ETL

* Cleans string columns (trim, casing normalization)
* Removes duplicates (`seller_id + item_id`)
* Validates price and stock
* Invalid records moved to **quarantine**
* Output written as a **Hudi table**

---

### 2️⃣ Company Sales ETL

* Cleans and validates sales data
* Handles malformed dates and negative values
* Supports incremental upserts
* Output written as a **Hudi table**

---

### 3️⃣ Competitor Sales ETL

* Normalizes seller and item identifiers
* Validates pricing and sales metrics
* Captures market-level performance
* Output written as a **Hudi table**

---

## 🚨 Quarantine Handling

Records failing data-quality checks are redirected to a **quarantine zone** containing:

* Dataset name
* Original record
* Failure reason (e.g. `missing_item_id`, `negative_price`)

This keeps analytical tables clean while preserving bad data for debugging.

---

## 📊 Recommendation Logic (Consumption Layer)

The consumption pipeline reads all three Hudi tables and performs:

1. **Top-selling item identification**

   * Within company data
   * Across competitor data

2. **Catalog gap analysis**

   * Identifies items missing from each seller’s catalog

3. **Revenue estimation**

   ```
   expected_units_sold =
     total_units_sold / number_of_sellers_selling_item

   expected_revenue =
     expected_units_sold × marketplace_price
   ```

---

## 📤 Final Output

A CSV file containing seller-level recommendations:

**Output Columns**

* `seller_id`
* `item_id`
* `item_name`
* `category`
* `market_price`
* `expected_units_sold`
* `expected_revenue`

This output is ready for **business consumption or dashboarding**.

---

## 🧩 Configuration (`ecomm_prod.yml`)

All input and output paths are externalized via YAML, making the pipeline environment-agnostic (local or cloud).

```yaml
seller_catalog:
  input_path: "<raw_path>/seller_catalog.csv"
  hudi_output_path: "<processed_path>/seller_catalog_hudi"

company_sales:
  input_path: "<raw_path>/company_sales.csv"
  hudi_output_path: "<processed_path>/company_sales_hudi"

competitor_sales:
  input_path: "<raw_path>/competitor_sales.csv"
  hudi_output_path: "<processed_path>/competitor_sales_hudi"

recommendation:
  seller_catalog_hudi: "<processed_path>/seller_catalog_hudi"
  company_sales_hudi: "<processed_path>/company_sales_hudi"
  competitor_sales_hudi: "<processed_path>/competitor_sales_hudi"
  output_csv: "<processed_path>/recommendations.csv"
```

---

## ▶️ Running the Pipelines

Each stage is executed independently using Spark submit scripts.

Example:

```bash
./scripts/etl_seller_catalog_spark_submit.sh
./scripts/etl_company_sales_spark_submit.sh
./scripts/etl_competitor_sales_spark_submit.sh
./scripts/consumption_recommendation_spark_submit.sh
```

---

## 🧠 Why This Project Matters

This project demonstrates:

* Real-world **data quality handling**
* Incremental data processing with **Apache Hudi**
* Medallion architecture design
* Translating raw sales data into **business recommendations**

It closely mirrors **production data engineering workflows** used in ecommerce and marketplace platforms.

---

## 📦 Datasets

The pipeline works with **three independent datasets**, each representing a different business view of the marketplace.
All datasets may contain **dirty or inconsistent records**, which are handled through cleaning, validation, and quarantine logic.

---

### 1️⃣ Seller Catalog Dataset

Represents the items currently listed by each seller on the platform.

**Purpose**

* Understand what each seller is already selling
* Identify missing high-performing items

**Key Columns**

* `seller_id` – Unique identifier of the seller
* `item_id` – Unique identifier of the product
* `item_name` – Product name (normalized during processing)
* `category` – Product category (standardized labels)
* `marketplace_price` – Seller’s listed price
* `stock_qty` – Available inventory

**Common Issues Handled**

* Missing or duplicate `(seller_id, item_id)`
* Inconsistent casing and whitespace
* Invalid or negative prices / stock values

---

### 2️⃣ Company Sales Dataset

Contains historical sales data for items sold on the platform.

**Purpose**

* Identify top-selling items within the company
* Estimate demand based on historical performance

**Key Columns**

* `item_id` – Sold product identifier
* `units_sold` – Number of units sold
* `revenue` – Total revenue generated
* `sale_date` – Date of sale

**Common Issues Handled**

* Negative or missing sales values
* Malformed or future dates
* Duplicate item-level records

---

### 3️⃣ Competitor Sales Dataset

Represents market-level sales performance from competitor sellers.

**Purpose**

* Identify products performing well outside the company
* Discover high-demand items missing from the platform

**Key Columns**

* `seller_id` – Competitor seller identifier
* `item_id` – Product identifier
* `units_sold` – Units sold by competitor
* `revenue` – Revenue generated
* `marketplace_price` – Competitor’s price
* `sale_date` – Date of sale

**Common Issues Handled**

* Missing seller or item identifiers
* Invalid prices or revenue values
* Date inconsistencies

---

### 🧪 Data Quality & Quarantine

Across all datasets:

* Records failing validation rules are **not discarded**
* They are redirected to a **quarantine zone** with:

  * Original record
  * Dataset name
  * Failure reason

This ensures clean analytical tables while preserving traceability.



## 🔮 Possible Enhancements

* Delta Lake / Iceberg comparison
* Incremental consumption layer
* Dashboarding (Superset / Power BI)
* Feature store integration
* Real-time ingestion (Kafka + Spark Streaming)
