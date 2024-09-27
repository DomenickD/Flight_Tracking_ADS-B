from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Sample data (replace with your actual data or database interactions)
items = {
    "foo": {"name": "Foo", "price": 50.0},
    "bar": {"name": "Bar", "price": 35.2},
    "baz": {"name": "Baz", "price": 27.9},
}


class Item(BaseModel):
    name: str
    price: float


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.post("/items/")
def create_item(item: Item):
    if item.name in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items[item.name] = item
    return item
