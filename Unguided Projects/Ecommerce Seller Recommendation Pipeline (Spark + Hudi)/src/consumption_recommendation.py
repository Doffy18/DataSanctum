import sys
import yaml
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, desc, broadcast, row_number, lit, countDistinct
from pyspark.sql.window import Window

def main(config_path):

    # Load config

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    seller_catalog_path = config['sellercatalog']['hudioutputpath']
    company_sales_path = config['companysales']['hudioutputpath']
    competitor_sales_path = config['competitorsales']['hudioutputpath']
    output_path = config['recommendations']['outputpath']

    spark = SparkSession.builder.appName("Seller_Item_Recommendations").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")


    # Load data

    seller_catalog = spark.read.format("hudi").load(seller_catalog_path)
    company_sales = spark.read.format("hudi").load(company_sales_path)
    competitor_sales = spark.read.format("hudi").load(competitor_sales_path)

    # Keep relevant columns
    seller_catalog = seller_catalog.select(
        "seller_id", "item_id", "item_name", "category", "marketplace_price"
    ).distinct()

    company_sales = company_sales.select("item_id", "units_sold", "revenue")
    competitor_sales = competitor_sales.select("item_id", "units_sold", "marketplace_price")

    seller_items = seller_catalog.select("seller_id", "item_id").distinct()
    all_sellers = seller_catalog.select("seller_id").distinct()


    # Aggregate company sales per item
    company_item_sales = company_sales.groupBy("item_id").sum("units_sold") \
        .withColumnRenamed("sum(units_sold)", "total_units_sold")

    # Count number of sellers selling each item
    sellers_per_item = seller_catalog.groupBy("item_id").agg(countDistinct("seller_id").alias("num_sellers"))

    # Calculate expected_units_sold = total_units_sold / number of sellers
    company_item_sales = company_item_sales.join(sellers_per_item, "item_id", "left") \
        .withColumn("expected_units_sold", col("total_units_sold") / col("num_sellers"))

    # Join category and other info
    company_item_info = seller_catalog.select("item_id", "item_name", "category", "marketplace_price").dropDuplicates(["item_id"])
    company_item_sales = company_item_sales.join(company_item_info, "item_id", "left")

    # Take top 10 items per category
    window_category = Window.partitionBy("category").orderBy(desc("expected_units_sold"))
    top_company_items = company_item_sales.withColumn("rank", row_number().over(window_category)) \
                                         .filter(col("rank") <= 10) \
                                         .drop("rank")

    # Recommend company top items missing for each seller
    company_recommend = all_sellers.crossJoin(broadcast(top_company_items)) \
        .join(seller_items, ["seller_id", "item_id"], "left_anti") \
        .withColumn("recommendation_source", lit("company")) \
        .withColumn("expected_revenue", col("marketplace_price") * col("expected_units_sold"))


    # Competitor top-selling items

    competitor_item_sales = competitor_sales.groupBy("item_id").sum("units_sold") \
        .withColumnRenamed("sum(units_sold)", "total_units_sold")

    competitor_prices = competitor_sales.groupBy("item_id").avg("marketplace_price") \
        .withColumnRenamed("avg(marketplace_price)", "competitor_price")

    # Count number of sellers selling each item in our catalog
    competitor_item_sales = competitor_item_sales.join(sellers_per_item, "item_id", "left") \
        .withColumn("expected_units_sold", col("total_units_sold") / col("num_sellers"))

    top_competitor_items = competitor_item_sales.join(competitor_prices, "item_id", "left") \
        .join(company_item_info.select("item_id", "item_name", "category"), "item_id", "left") \
        .orderBy(desc("expected_units_sold")).limit(10)

    # Recommend competitor top items missing for each seller
    competitor_recommend = all_sellers.crossJoin(broadcast(top_competitor_items)) \
        .join(seller_items, ["seller_id", "item_id"], "left_anti") \
        .withColumn("marketplace_price", col("competitor_price")) \
        .withColumn("recommendation_source", lit("competitor")) \
        .withColumn("expected_revenue", col("marketplace_price") * col("expected_units_sold"))


    # Combine recommendations

    common_cols = ["seller_id", "item_id", "item_name", "category", "marketplace_price",
                   "expected_units_sold", "expected_revenue", "recommendation_source"]
    company_recommend = company_recommend.select(common_cols)
    competitor_recommend = competitor_recommend.select(common_cols)

    recommendations = company_recommend.unionByName(competitor_recommend) \
        .dropDuplicates(["seller_id", "item_id"])

    # Rank by expected revenue per seller and take top 10
    window_spec = Window.partitionBy("seller_id").orderBy(desc("expected_revenue"))
    recommendations = recommendations.withColumn("rank", row_number().over(window_spec)) \
                                     .filter(col("rank") <= 10) \
                                     .drop("rank")


    # Write recommendations to CSV

    recommendations.write.mode("overwrite").option("header", True).csv(output_path)
    print("Recommendations generated successfully.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python consumption_recommendation.py <config_path>")
        sys.exit(-1)
    main(sys.argv[1])

