from pydantic import BaseModel

from db import Session
from db.models import Camera

from .router import router


class CameraPayload(BaseModel):
    id: str
    address: str
    lat: float
    alt: float


@router.post('/cameras')
async def handler(payload: CameraPayload):
    async with Session() as db_session:
        camera = Camera(id=payload.id, address=payload.address, 
                        lat=payload.lat, alt=payload.alt)
        db_session.add(camera)
        db_session.commit()

    return payload
