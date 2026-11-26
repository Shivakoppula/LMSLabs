import pytest
from fastapi.testclient import TestClient

from app.main import app, get_order_service
from app.repository import InMemoryOrderRepository
from app.service import OrderService


@pytest.fixture
def client():
    service = OrderService(InMemoryOrderRepository())
    app.dependency_overrides[get_order_service] = lambda: service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.pop(get_order_service, None)


def sample_order() -> dict:
    return {
        "customer_name": "Anu",
        "items": [
            {"name": "Notebook", "quantity": 2, "unit_price": 50},
            {"name": "Pen", "quantity": 1, "unit_price": 20},
        ],
    }


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_order_returns_expected_order(client: TestClient) -> None:
    response = client.post("/orders", json=sample_order())

    assert response.status_code == 201
    assert response.json()["order_id"] == 1
    assert response.json()["customer_name"] == "Anu"
    assert response.json()["total"] == 120.0


def test_list_orders_returns_saved_order(client: TestClient) -> None:
    client.post("/orders", json=sample_order())

    response = client.get("/orders")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["order_id"] == 1
    assert response.json()[0]["total"] == 120.0


@pytest.mark.parametrize(
    "invalid_order",
    [
        pytest.param(
            {
                "customer_name": "Anu",
                "items": [
                    {"name": "Notebook", "quantity": 0, "unit_price": 50}
                ],
            },
            id="zero-quantity",
        ),
        pytest.param(
            {
                "customer_name": "Anu",
                "items": [
                    {"name": "Notebook", "quantity": -1, "unit_price": 50}
                ],
            },
            id="negative-quantity",
        ),
        pytest.param(
            {
                "customer_name": "Anu",
                "items": [
                    {"name": "Notebook", "quantity": 1, "unit_price": -1}
                ],
            },
            id="negative-unit-price",
        ),
        pytest.param({"customer_name": "Anu", "items": []}, id="empty-items"),
        pytest.param(
            {
                "items": [
                    {"name": "Notebook", "quantity": 1, "unit_price": 50}
                ]
            },
            id="missing-customer-name",
        ),
        pytest.param({"customer_name": "Anu"}, id="missing-items"),
    ],
)
def test_invalid_order_input_returns_validation_error(
    client: TestClient,
    invalid_order: dict,
) -> None:
    response = client.post("/orders", json=invalid_order)

    assert response.status_code == 422


def test_zero_unit_price_is_accepted(client: TestClient) -> None:
    order = {
        "customer_name": "Anu",
        "items": [{"name": "Notebook", "quantity": 1, "unit_price": 0}],
    }

    response = client.post("/orders", json=order)

    assert response.status_code == 201
    assert response.json()["total"] == 0.0