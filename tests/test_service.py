from app.models import OrderRequest
from app.repository import InMemoryOrderRepository
from app.service import OrderService


def sample_order() -> OrderRequest:
    return OrderRequest(
        customer_name="Anu",
        items=[
            {"name": "Notebook", "quantity": 2, "unit_price": 50},
            {"name": "Pen", "quantity": 1, "unit_price": 20},
        ],
    )


def test_calculate_total_rounds_to_two_decimals() -> None:
    service = OrderService(InMemoryOrderRepository())

    total = service.calculate_total(sample_order().items)

    assert total == 120.0


def test_create_order_can_be_listed() -> None:
    service = OrderService(InMemoryOrderRepository())

    created_order = service.create_order(sample_order())
    orders = service.list_orders()

    assert created_order.order_id == 1
    assert orders == [created_order]