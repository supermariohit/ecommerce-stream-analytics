from dataclasses import dataclass
from datetime import datetime, timezone
from random import Random
from typing import Sequence
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Product:
    product_id: int
    category: str
    price: float


@dataclass(frozen=True)
class Customer:
    user_id: int
    city: str
    segment: str


@dataclass(frozen=True)
class Order:
    order_id: UUID
    user_id: int
    product_id: int
    ts: datetime
    city: str
    category: str
    price: float
    quantity: int
    amount: float
    status: str
    payment_method: str


class OrderGenerator:
    def __init__(
        self,
        products: Sequence[Product],
        customers: Sequence[Customer],
        seed: int,
    ) -> None:
        if not products or not customers:
            raise ValueError("Product and customer catalogs must not be empty")

        self._products = tuple(products)
        self._customers = tuple(customers)
        segment_weights = {"new": 1, "regular": 3, "vip": 5}
        self._customer_weights = [
            segment_weights.get(customer.segment, 1) for customer in self._customers
        ]
        self._random = Random(seed)

    def generate_batch(self, size: int, ts: datetime) -> list[Order]:
        if size < 0:
            raise ValueError("Batch size must be non-negative")
        if ts.utcoffset() is None:
            raise ValueError("Batch timestamp must include a time zone")

        timestamp = ts.astimezone(timezone.utc).replace(microsecond=0)
        customers = self._random.choices(self._customers, self._customer_weights, k=size)
        orders = []
        for customer in customers:
            product = self._random.choice(self._products)
            quantity = self._random.choices((1, 2, 3, 4), (70, 20, 8, 2))[0]
            status = self._random.choices(("paid", "pending", "cancelled"), (85, 10, 5))[0]
            payment = self._random.choices(("card", "sbp", "cash"), (65, 25, 10))[0]
            price = round(product.price, 2)
            orders.append(
                Order(
                    order_id=uuid4(),
                    user_id=customer.user_id,
                    product_id=product.product_id,
                    ts=timestamp,
                    city=customer.city,
                    category=product.category,
                    price=price,
                    quantity=quantity,
                    amount=round(price * quantity, 2),
                    status=status,
                    payment_method=payment,
                )
            )
        return orders
