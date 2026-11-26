from collections.abc import Sequence

from app.models import OrderItem, OrderRequest, OrderResponse
from app.repository import OrderRepository


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    def calculate_total(self, items: Sequence[OrderItem]) -> float:
        return round(sum(item.quantity * item.unit_price for item in items), 2)

    def create_order(self, order: OrderRequest) -> OrderResponse:
        total = self.calculate_total(order.items)
        return self._repository.save(order, total)

    def list_orders(self) -> list[OrderResponse]:
        return self._repository.list_all()