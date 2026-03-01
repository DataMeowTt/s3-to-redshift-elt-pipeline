from pyspark.sql import SparkSession
from pyspark.sql.functions import year, to_date, col

INPUT_PATH = "s3a://e-commerce-raw-data/bronze/List_of_Orders.csv"
OUTPUT_PATH = "s3a://e-commerce-raw-data/silver/List_of_Orders"

spark = SparkSession.builder.appName("Partition List of Orders By Year").getOrCreate()

df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(INPUT_PATH)

df = df.withColumn(
    "year",
    year(to_date(col("Order Date"), "yyyy-MM-dd"))
)

df.write \
    .partitionBy("year") \
    .mode("overwrite") \
    .parquet(OUTPUT_PATH)

spark.stop()