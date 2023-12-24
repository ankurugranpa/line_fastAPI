import os
import uuid
import base64


from azure.storage.blob.aio import BlobServiceClient
from  dotenv import load_dotenv

from fastapi import APIRouter
from api.schemas import blob as blob_schema


router = APIRouter(
    prefix='/blob',
    tags=['Blob']
)

load_dotenv()
AZURE_CONNECTION_STRING = os.environ.get('Azure_CONNNECTION_STRING')
AZURE_BLOB_BASE_URL = os.environ.get('AZURE_BLOB_BASE_URL')

# @router.post("/url", responses=blob_schema.GetBlobUrlResponse)
# async  def base2url(blob_body:  blob_schema.GetBlobUrl):
#     blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
#     container_name = "blob-test"
#     blob_name = f"{uuid.uuid4()}.mp3"
#     binary_data = base64.b64decode(blob_body.base64_binary)
#     container_client = blob_service_client.get_container_client(container=container_name)
#     await container_client.upload_blob(name=blob_name, data=binary_data)
#     upload_url = f"{AZURE_BLOB_BASE_URL}/{container_name}/{blob_name}"
#     return upload_url
