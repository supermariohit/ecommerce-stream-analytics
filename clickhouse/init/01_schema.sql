-- База
CREATE DATABASE IF NOT EXISTS ecommerce;

-- Справочник товаров
CREATE TABLE IF NOT EXISTS ecommerce.products (
    product_id UInt32,
    name       String,
    category   LowCardinality(String),
    price      Float32,
    stock      UInt32
) ENGINE = ReplacingMergeTree()
ORDER BY product_id;

-- Справочник пользователей
CREATE TABLE IF NOT EXISTS ecommerce.users (
    user_id       UInt32,
    name          String,
    city          LowCardinality(String),
    segment       LowCardinality(String),
    registered_at DateTime
) ENGINE = ReplacingMergeTree()
ORDER BY user_id;

-- Поток заказов
CREATE TABLE IF NOT EXISTS ecommerce.orders (
    order_id       UUID,
    user_id        UInt32,
    product_id     UInt32,
    ts             DateTime,
    city           LowCardinality(String),
    category       LowCardinality(String),
    price          Float32,
    quantity       UInt16,
    amount         Float32,
    status         LowCardinality(String),
    payment_method LowCardinality(String)
) ENGINE = MergeTree()
PARTITION BY toDate(ts)
ORDER BY (city, category, ts, user_id)
TTL toDateTime(ts) + INTERVAL 90 DAY;