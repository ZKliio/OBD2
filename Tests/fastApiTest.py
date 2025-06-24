from typing import Union

from fastapi import FastAPI

from pydantic import BaseModel # declares objects and classes

app = FastAPI()

# In-memory storage for items
fake_db = {}

#declare object Item as a class
class Item(BaseModel):
    item_id: int
    name: str
    description: Union[str, None] = None
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
async def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, 
#             "description": Item.description,
#             "q": q
#             }

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    item = fake_db.get(item_id)
    if item:
        return {"item_id": item_id, "item": item, "q": q}
    else:
        return {"error": "Item not found"}
    
@app.get("/items/")
async def read_item(item_id: int, fake_db: dict, q: Union[str, None] = None):
    if item in fake_db:
            for item in fake_db:
                return {"item_id": item_id, "item": item, "q": q}
    else:
        return {"error": "Item not found"}



# @app.put("/items/{item_id}")
# def update_item(item: Item, item_id: int, ):
#     return {"item_name": item.name, "item_id": item_id, 
#             "item_price": item.price,
#             "item_description": item.description
#             }


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    fake_db[item_id] = item.dict()  # Convert Item model to dictionary for storage
    return {"message": "Item updated", "item": fake_db[item_id]}