## Overview

This project demonstrates an end-to-end Data Engineering pipeline built on AWS.  
The goal is to design a scalable architecture that ingests raw CSV datasets into Amazon S3, processes and optimizes them using a layered data lake approach, and loads the transformed data into Amazon Redshift using a Star Schema model for analytics.

---

# Architecture
Local CSV Files
↓
Amazon S3 (Bronze Layer - Raw Data)
↓
Amazon S3 (Silver Layer - Transformed & Partitioned)
↓
Amazon Redshift (Star Schema Data Warehouse)

---

# Data Lake Design (Amazon S3)

The data lake is structured into two layers:

## Bronze Layer (Raw Zone)

- Stores original CSV files without modification
- Acts as the immutable source of truth
- Preserves raw schema and structure
- Enables reprocessing if needed

Example structure:
s3://bucket/bronze/
├── list_of_orders.csv
├── order_detail.csv
└── sales_target.csv

---

## Silver Layer (Cleaned & Optimized Zone)

- Data is transformed and standardized
- Schema inconsistencies are resolved
- The `list_of_orders` dataset is partitioned by **year** to optimize query performance
- Stored in optimized format (e.g., Parquet)

Example structure:
s3://bucket/silver/list_of_orders/
├── year=2022/
├── year=2023/
└── year=2024/

### Why Partition by Year?

- Reduces data scanned during queries  
- Improves performance  
- Lowers query cost  
- Aligns with common BI time-based filtering  

---

# Data Warehouse Design (Amazon Redshift)

The data is loaded from S3 into Amazon Redshift using the `COPY` command and modeled using a **Star Schema**.

## ⭐ Star Schema Model

The warehouse consists of:

### Dimension Tables

- `dim_customer`
- `dim_product`
- `dim_date`

These tables:
- Store descriptive attributes
- Use surrogate keys
- Are configured with `DISTSTYLE ALL` for performance optimization

---

### Fact Table

- `fact_sales`

This table:
- Contains measurable business metrics (amount, profit, quantity)
- References dimension tables using foreign keys
- Uses:
  - `DISTKEY (customer_id)` to optimize joins
  - `SORTKEY (order_date)` to optimize time-based filtering

---

# Data Flow

1. Upload raw CSV files to S3 Bronze.
2. Transform and partition selected datasets into Silver.
3. Use Redshift `COPY` to load data into staging tables.
4. Insert data into dimension tables (deduplicated).
5. Populate fact table using JOINs between staging and dimension tables.
6. Serve data for BI and analytical workloads.

---

# 📈 Future Improvements

- Introduce data quality checks
- Add BI visualization layer (Power BI / Superset)
