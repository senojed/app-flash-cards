import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
from app.config import settings

MEDIA_ROOT = Path("/media")


async def save_media(card_id: uuid.UUID, label: str, file: UploadFile) -> str:
    ext = Path(file.filename).suffix.lower()
    allowed = {".png", ".jpg", ".jpeg", ".webp", ".mp3", ".ogg"}
    if ext not in allowed:
        raise HTTPException(400, f"Unsupported file type: {ext}")

    content = await file.read()
    max_bytes = settings.media_max_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(400, f"File too large (max {settings.media_max_size_mb} MB)")

    dir_path = MEDIA_ROOT / str(card_id)
    dir_path.mkdir(parents=True, exist_ok=True)
    file_path = dir_path / f"{label}{ext}"
    file_path.write_bytes(content)

    return f"{card_id}/{label}{ext}"


def delete_media(card_id: uuid.UUID):
    import shutil
    dir_path = MEDIA_ROOT / str(card_id)
    if dir_path.exists():
        shutil.rmtree(dir_path)
