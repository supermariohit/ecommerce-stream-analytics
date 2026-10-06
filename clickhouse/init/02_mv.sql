CREATE TABLE IF NOT EXISTS ecommerce.orders_agg_1m (
    minute        DateTime,
    city          LowCardinality(String),
    category      LowCardinality(String),
    orders_count  UInt64,
    items_sold    UInt64,
    revenue       Float64,
    avg_order_value AggregateFunction(avg, Float64),
    cancelled_count UInt64
) ENGINE = AggregatingMergeTree()
PARTITION BY toDate(minute)
ORDER BY (minute, city, category);

CREATE MATERIALIZED VIEW IF NOT EXISTS ecommerce.mv_orders_1m
TO ecommerce.orders_agg_1m AS
SELECT
    toStartOfMinute(ts) AS minute,
    city,
    category,
    count()                        AS orders_count,
    sum(quantity)                  AS items_sold,
    sum(amount)                    AS revenue,
    avgState(amount)               AS avg_order_value,
    countIf(status = 'cancelled')  AS cancelled_count
FROM ecommerce.orders
GROUP BY minute, city, category;