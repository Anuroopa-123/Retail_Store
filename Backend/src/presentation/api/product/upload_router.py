import os
import uuid
import shutil

from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

router = APIRouter(
    prefix="/product-upload",
    tags=["Product Upload"]
)

BASE_DIR = Path(__file__).resolve().parents[4]

UPLOAD_FOLDER = BASE_DIR / "uploads" / "product_images"

UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


@router.post("/")
async def upload_product_image(

    file: UploadFile = File(...)

):

    if not file.content_type.startswith("image/"):

        raise HTTPException(

            status_code=400,

            detail="Only image files allowed"

        )

    extension = file.filename.split(".")[-1]

    filename = f"{uuid.uuid4()}.{extension}"

    filepath = UPLOAD_FOLDER / filename

    with open(filepath, "wb") as buffer:

        shutil.copyfileobj(

            file.file,

            buffer

        )

    return {

    "filename": filename,

    "image_url": f"/uploads/product_images/{filename}"

}