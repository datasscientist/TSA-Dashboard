from fastapi import APIRouter
from typing import List
from .models import Item, ItemResponse

router = APIRouter()

@router.post("/items/", response_model=ItemResponse)
async def create_item(item: Item):
    return ItemResponse(id=1, name=item.name, description=item.description)

@router.get("/items/", response_model=List[ItemResponse])
async def read_items():
    return [ItemResponse(id=1, name="Sample Item", description="This is a sample item.")]