from random import randint
from datetime import datetime, timedelta

from sqlalchemy.sql.expression import update
from db import Session
from db.models import Camera, GarbageLog

from .router import router
import pandas as pd


@router.post('/fill-dummy-data')
async def fill_with_dummy_data():
    df = pd.read_csv('handlers/cameras-data.csv').dropna()
    async with Session() as db_session:
        for i, row in enumerate(df.iloc):
            if None in row:
                continue
            camera = Camera(
                id=i + 1,
                lat=row['Latitude'], alt=row['Longitude'],
                address=row['Адрес установки камеры'])
            db_session.add(camera)
        await db_session.commit()

        for i in range(len(df)):
            time = datetime(2021, 11, 25)
            total_containers = randint(4, 10)
            for _ in range(6 * 24 * 10):
                filled_containers = randint(
                    total_containers - 2, total_containers)
                garbage_log = GarbageLog(
                    camera_id=i + 1,
                    total_containers_count=total_containers,
                    filled_containers_count=filled_containers,
                    created_at=time,
                    updated_at=time,
                    garbage_containers_data=[{"insideGarbage": randint(
                        0, 3), "nearbyGarbage": randint(0, 4)} for _ in range(total_containers)]
                )
                time += timedelta(minutes=10)
                db_session.add(garbage_log)
            await db_session.commit()
