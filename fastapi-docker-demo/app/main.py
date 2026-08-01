from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Simple FastAPI Demo",
    description="A minimal FastAPI app packaged with Docker Compose and CI/CD",
    version="1.0.0",
)


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True


# In-memory "database" just for demo purposes
items_db = {}


@app.get("/")
def read_root():
    return {"message": "Welcome to the Simple FastAPI Demo"}


@app.get("/health")
def health_check():
    """Used by Docker healthcheck and CI smoke tests."""
    return {"status": "ok"}


@app.get("/items")
def list_items():
    return items_db


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items_db:
        return {"error": "Item not found"}
    return items_db[item_id]


@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    items_db[item_id] = item
    return {"item_id": item_id, "item": item}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id in items_db:
        del items_db[item_id]
        return {"message": "Item deleted"}
    return {"error": "Item not found"}
