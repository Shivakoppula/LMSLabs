from fastapi import Depends, FastAPI, status

from app.models import OrderRequest, OrderResponse
from app.repository import InMemoryOrderRepository
from app.service import OrderService

app = FastAPI()

repository = InMemoryOrderRepository()
order_service = OrderService(repository)


def get_order_service() -> OrderService:
    return order_service


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order: OrderRequest,
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    return service.create_order(order)


@app.get("/orders", response_model=list[OrderResponse])
def list_orders(
    service: OrderService = Depends(get_order_service),
) -> list[OrderResponse]:
    return service.list_orders()