from typing import Protocol

from app.models import OrderRequest, OrderResponse


class OrderRepository(Protocol):
    def save(self, order: OrderRequest, total: float) -> OrderResponse:
        ...

    def list_all(self) -> list[OrderResponse]:
        ...


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self._orders: list[OrderResponse] = []

    def save(self, order: OrderRequest, total: float) -> OrderResponse:
        saved_order = OrderResponse(
            order_id=len(self._orders) + 1,
            customer_name=order.customer_name,
            items=order.items,
            total=total,
        )
        self._orders.append(saved_order)
        return saved_order

    def list_all(self) -> list[OrderResponse]:
        return list(self._orders)