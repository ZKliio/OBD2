from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List

app = FastAPI()

# MongoDB setup
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.mydatabase
collection = db.items

# Helper to convert ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

# Pydantic model
class Item(BaseModel):
    id: str
    # id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    description: Optional[str] = None
    price: float
    is_offer: Optional[bool] = None

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
def item_serializer(item):
    return {
        "id": str(item["_id"]),  # Rename and convert
        "name": item["name"],
        "price": item["price"]
    }

# # Create item (POST or PUT)
# @app.put("/items/{item_id}")
# async def update_item(item_id: str, item: Item):
#     item_dict = item.dict(by_alias=True)
#     item_dict["_id"] = ObjectId(item_id)
#     await collection.replace_one({"_id": ObjectId(item_id)}, item_dict, upsert=True)
#     return {"message": "Item stored", "item": item_dict}

# Get item
@app.get("/items/{id}")
async def read_item(id: str):
    item = await collection.find_one({"_id": ObjectId(id)})
    if item:
        return Item(**item)
    raise HTTPException(status_code=404, detail="Item not found")

# # Convert mongo object to dict
# def item_serializer(item) -> dict:
#     item["_id"] = str(item["_id"])
#     return item

# @app.get("/items", response_model=List[dict])
# async def get_items():
#     items = []
#     async for item in collection.find():
#         items.append(item_serializer(item))
#     return items
@app.get("/items", response_model=List[Item])
async def get_items():
    items = []
    async for item in collection.find():
        items.append(Item(**item))
    return items