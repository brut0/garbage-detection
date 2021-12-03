from datetime import datetime
from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, func

from .models import GarbageLog, Camera


class Selector:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def select_littered_points(self) -> Tuple[Camera, int, datetime]:
        statement = select(
            Camera, 
            func.last_value(GarbageLog.garbage_index).over(
                order_by=GarbageLog.created_at, 
                partition_by=GarbageLog.camera_id,
                range_=(None, None)
            ).label('current_garbage_index'), 
            func.last_value(GarbageLog.created_at).over(
                order_by=GarbageLog.created_at, 
                partition_by=GarbageLog.camera_id,
                range_=(None, None)
            ).label('time')
        ).join(
            GarbageLog, 
            isouter=True
        ).where(
            GarbageLog.garbage_index > 1
        )
        result = await self.session.execute(statement)
        return result.all()
