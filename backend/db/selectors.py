from typing import Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, func
from sqlalchemy.sql.expression import case, desc, cast
from sqlalchemy.types import Float

from .models import GarbageLog, Camera


class Selector:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def select_cameras(self) -> Tuple[Camera, int, int, list]:
        statement = select(
            Camera, 
            func.last_value(GarbageLog.total_containers_count).over(
                order_by=GarbageLog.created_at, 
                partition_by=GarbageLog.camera_id,
                range_=(None, None)
            ), 
            func.last_value(GarbageLog.filled_containers_count).over(
                order_by=GarbageLog.created_at, 
                partition_by=GarbageLog.camera_id,
                range_=(None, None)
            ),
            func.last_value(GarbageLog.garbage_containers_data).over(
                order_by=GarbageLog.created_at, 
                partition_by=GarbageLog.camera_id,
                range_=(None, None)
            ),
        ).join(
            GarbageLog, 
            isouter=True
        ).distinct()
        result = await self.session.execute(statement)
        return result.all()

    async def select_camera_with_id(self, camera_id: int) -> Optional[Camera]:
        statement = select(Camera).where(Camera.id == camera_id)
        result = await self.session.execute(statement)
        return result.scalar()

    async def select_top5(self) -> Tuple[Camera, int, int, list]:
        substatement = select(
            GarbageLog, 
            case([(GarbageLog.total_containers_count != 0, 
                   cast(GarbageLog.filled_containers_count, Float) / cast(GarbageLog.total_containers_count, Float))], 
                 else_=0).label('fulliness')
        ).subquery()
        statement = select(
            Camera, 
            func.last_value(substatement.c.fulliness).over(
                order_by=substatement.c.created_at, 
                partition_by=substatement.c.camera_id,
                range_=(None, None)
            ).label('fulliness'), 
            func.last_value(substatement.c.filled_containers_count).over(
                order_by=substatement.c.created_at, 
                partition_by=substatement.c.camera_id,
                range_=(None, None)
            ).label('filled_containers'),
            func.last_value(substatement.c.garbage_containers_data).over(
                order_by=substatement.c.created_at, 
                partition_by=substatement.c.camera_id,
                range_=(None, None)
            ),
        ).join(
            substatement, 
            Camera.id == substatement.c.camera_id, 
            isouter=True
        ).order_by(
            desc('fulliness'), 
            desc('filled_containers')
        ).distinct().limit(5)
        result = await self.session.execute(statement)
        return result.all()
