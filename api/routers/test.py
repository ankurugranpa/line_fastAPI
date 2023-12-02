from fastapi import APIRouter

import api.schemas.task as task_scheam

roter = APIRouter()

@roter.get("tastk")
async def list_task():
   pass 
