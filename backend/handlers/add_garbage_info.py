from pydantic import BaseModel
from sqlalchemy.orm import session

from db import Session
from db.models import GarbageLog

from .router import router


class SingleCameraInfo(BaseModel):
    cameraId: int
    garbageIndex: int


@router.post('/add-garbage-info')
async def handler(info: SingleCameraInfo):
    async with Session() as db_session:
        obj = GarbageLog(camera_id=info.cameraId, 
                         garbage_index=info.garbageIndex)
        db_session.add(obj)
        await db_session.commit()
