from datetime import datetime
from typing import Tuple

from db import Session, Selector
from db.models import Camera

from .router import router


def serialize_point(point: Tuple[Camera, int, datetime]):
    camera, garbage_index, time_ = point
    return {'cameraId': camera.id,
            'garbageIndex': garbage_index,
            'time': time_,
            'location': [camera.lat, camera.alt]}


@router.get('/littered-points')
async def handler():
    async with Session() as db_session:
        selector = Selector(db_session)
        points = await selector.select_littered_points()

    return {'data': list(map(serialize_point, points))}
