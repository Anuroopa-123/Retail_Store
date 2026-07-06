import os
import uuid
import shutil

from fastapi import APIRouter, UploadFile, File

router = APIRouter(
    prefix="/product-upload",
    tags=["Product Upload"]
)

UPLOAD_FOLDER = "uploads/product_images"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@router.post("/")
async def upload_product_image(

    file: UploadFile = File(...)

):

    extension = file.filename.split(".")[-1]

    filename = f"{uuid.uuid4()}.{extension}"

    filepath = os.path.join(

        UPLOAD_FOLDER,

        filename

    )

    with open(filepath, "wb") as buffer:

        shutil.copyfileobj(

            file.file,

            buffer

        )

    return {

        "filename": filename,

        "image_url": f"/uploads/product_images/{filename}"

    }