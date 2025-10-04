from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Lab 3 Backend Service", version="1.0.0")

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

# In-memory "база данных"
items_db = []

@app.get("/")
async def read_root():
    return {"message": "Добро пожаловать в Backend Service Lab 3!"}

@app.get("/items/")
async def read_items():
    return {"items": items_db, "count": len(items_db)}

@app.post("/items/")
async def create_item(item: Item):
    items_db.append(item.dict())
    return {"message": "Item created", "item": item}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if 0 <= item_id < len(items_db):
        return items_db[item_id]
    return {"error": "Item not found"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)