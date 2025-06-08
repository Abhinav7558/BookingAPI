from fastapi import APIRouter

router = APIRouter(
    prefix="/bookings",
    tags=['bookings']
)

@router.get("/bookings")
async def get_bookings():
    return "Done"