from fastapi import APIRouter

router = APIRouter(
    prefix="/classes",
    tags=['classes']
)

@router.get("/classes")
async def get_bookings():
    return "Done"

