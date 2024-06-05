from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.items import Item


class ItemsCrud:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_items(self, skip: int = 0, limit: int = 100) -> List[Item]:
        items: List[Item] = (
            await self._db.scalars(select(Item).offset(skip).limit(limit))
        ).all()
        return items

    async def create_item(self, item: Item) -> Item:
        self._db.add(item)
        self._db.commit()  # Can be placed on manager level instead to improve commit performance
        self._db.refresh(item)
        return item
