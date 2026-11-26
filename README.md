# CommerceHub Order API

This project implements the two CommerceHub hands-on guides in the Phase 4 workspace.

## Architecture

- `app/main.py` owns the three HTTP endpoints and injects one shared `OrderService` with FastAPI `Depends()`.
- `app/service.py` owns order orchestration and the `calculate_total()` business rule.
- `app/repository.py` defines the `OrderRepository` Protocol and provides the in-memory `InMemoryOrderRepository` implementation with sequential IDs.
- `app/models.py` validates order input and defines response schemas; it contains no pricing calculations.
- `tests/` covers the API contract, input validation, total calculation, and persistence through the service.

This follows SRP by keeping HTTP handling, calculations, and storage separate. Dependency Inversion makes `OrderService` depend on the repository Protocol; FastAPI dependency injection supplies the shared in-memory implementation.

## Run and verify

From this directory, create the local environment, install dependencies, and run the tests and API:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -v
.venv/bin/python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`, expand an endpoint, select **Try it out**, enter the request body when prompted, then select **Execute**. Test `GET /health`, submit the valid order below to `POST /orders`, and use `GET /orders` to retrieve it. A quantity of `0` returns HTTP 422.

```json
{
	"customer_name": "Shiva",
	"items": [
		{"name": "Notebook", "quantity": 2, "unit_price": 50},
		{"name": "Pen", "quantity": 1, "unit_price": 20}
	]
}
```

The sample order returns total `120.0`. Orders are held in memory and are cleared when the server restarts.
