from typing import Tuple
from urllib.parse import urljoin

from db import Session, Selector
from db.models import Camera

from .router import router


def serialize_camera(point: Tuple[Camera, int, int]):
    camera, total_containers, filled_containers, containers_data = point
    photo = urljoin('/cameras', camera.photo_path) if camera.photo_path else None
    return {'id': camera.id,
            'address': camera.address, 
            'photo': photo,
            'location': [camera.lat, camera.alt], 
            'totalContainers': total_containers, 
            'filledContainers': filled_containers, 
            'containers': containers_data}


@router.get('/cameras')
async def handler():
    async with Session() as db_session:
        selector = Selector(db_session)
        points = await selector.select_cameras()

    return {'data': list(map(serialize_camera, points))}
