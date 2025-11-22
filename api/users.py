import fastapi

router = fastapi.APIRouter()

@router.get("/users/me")
async def read_current_user():
    return {"user_id": "the current user"}