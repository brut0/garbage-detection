from typing import Callable

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import settings


engine = create_async_engine(settings.Database.get_url())

Session: Callable[[], AsyncSession] = sessionmaker(bind=engine, 
                                                   class_=AsyncSession, 
                                                   expire_on_commit=False)
