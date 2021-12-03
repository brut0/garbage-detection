from random import randint

from db import Session
from db.models import Camera, GarbageLog

from .router import router


@router.post('/fill-dummy-data')
async def fill_with_dummy_data():
    async with Session() as db_session:
        for camera_id in range(1000, 1010):
            lat = 55.786778667350575 + float(randint(-1000, 1000)) / 10000
            alt = 49.12538845509848 + float(randint(-1000, 1000)) / 10000
            camera = Camera(
                id=camera_id, 
                lat=lat, alt=alt, 
                address='Казань',
                photo_path='photos/Garbage.jpg')
            db_session.add(camera)
            await db_session.commit()

            total_containers = randint(0, 10)
            filled_containers = randint(0, total_containers)
            garbage_log = GarbageLog(camera_id=camera.id, 
                                     total_containers_count=total_containers, 
                                     filled_containers_count=filled_containers)
            db_session.add(garbage_log)
            await db_session.commit()
