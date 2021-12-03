from datetime import datetime
from typing import Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, func

from .models import GarbageLog, Camera


class Selector:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def select_cameras(self) -> Tuple[Camera, int, int]:
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
            )
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
