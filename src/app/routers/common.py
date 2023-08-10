from fastapi import APIRouter

router = APIRouter(tags=[], responses={404: {"message": "Not found"}})


@router.get("/health")
async def health() -> dict:
    return {"status": "UP"}
