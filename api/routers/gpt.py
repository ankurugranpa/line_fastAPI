from fastapi import APIRouter

router = APIRouter()


@router.get("/task")
async def list_tasks():
    pass


@router.post("/gpt_ask")
async def ask_gpt():
    pass

