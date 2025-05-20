from fastapi import APIRouter

router = APIRouter()

@router.get("/data")
async def get_data():
    """Return sample data"""
    return {
        "message": "Data endpoint is working",
        "data": {
            "sample": "value",
            "items": [1, 2, 3]
        }
    }

# Add more endpoints as needed