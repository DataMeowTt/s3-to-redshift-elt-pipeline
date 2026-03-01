CREATE TABLE dim_product (
    product_id IDENTITY(1,1),
    category VARCHAR,
    sub_category VARCHAR
)
DISTSTYLE ALL;