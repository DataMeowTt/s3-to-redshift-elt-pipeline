CREATE TABLE fact_sales (
    order_id VARCHAR,
    order_date DATE,
    customer_id VARCHAR,
    product_id INT,
    quantity INT,
    amount DECIMAL(10,2),
    profit DECIMAL(10,2)
)
DISTKEY (customer_id)
SORTKEY (order_date);