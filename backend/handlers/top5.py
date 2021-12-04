from functools import reduce

from db import Selector, Session

from .router import router


@router.get('/cameras/top5')
async def handler():
    async with Session() as db_session:
        selector = Selector(db_session)
        top5 = await selector.select_top5()
        return [{'id': camera.id, 
                 'address': camera.address, 
                 'location': [camera.lat, camera.alt], 
                 'fullness': fullness * 100, 
                 'nearbyGarbage': reduce(lambda x, y: x + y['nearbyGarbage'], containers, 0)} 
                for camera, fullness, filled_containers, containers in top5]
