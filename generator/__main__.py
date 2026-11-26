import argparse
import json
import os
from dataclasses import asdict
from datetime import datetime, timezone

from .orders import Customer, OrderGenerator, Product


def main() -> None:
    parser = argparse.ArgumentParser(description="Preview one batch of e-commerce orders")
    parser.add_argument("--batch-size", type=int, default=os.getenv("BATCH_SIZE", "5"))
    parser.add_argument("--seed", type=int, default=os.getenv("SEED", "42"))
    args = parser.parse_args()

    # Use a subset of the ClickHouse seed rows to preview orders without a connection.
    products = (
        Product(1, "electronics", 299.99),
        Product(11, "books", 35.00),
        Product(31, "food", 24.90),
    )
    customers = (
        Customer(1, "Москва", "new"),
        Customer(2, "Санкт-Петербург", "regular"),
        Customer(3, "Новосибирск", "vip"),
    )
    generator = OrderGenerator(products, customers, args.seed)
    try:
        orders = generator.generate_batch(args.batch_size, datetime.now(timezone.utc))
    except ValueError as error:
        parser.error(str(error))

    for order in orders:
        print(json.dumps(asdict(order), default=str, ensure_ascii=False))


if __name__ == "__main__":
    main()
