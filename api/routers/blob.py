from fastapi import APIRouter
from api.schemas import blob as blob_schema

router = APIRouter()

# @router.post("/get-url/")
# def get_url(blob_body:blob_schema.GetBlobUrl):
    # return blob_schema.GetBlobUrlResponse(url="url", type="image")
    # return 0