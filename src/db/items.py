from typing import List, Any, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.items import Item


class ItemsCrud:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_items(self, skip: int = 0, limit: int = 100) -> List[Item]:
        items: Sequence[Any] = (
            await self._db.scalars(select(Item).offset(skip).limit(limit))
        ).all()
        return list(items)

    async def create_item(self, item: Item) -> Item:
        self._db.add(item)
        await self._db.commit()  # Can be placed on manager level instead to improve commit performance
        await self._db.refresh(item)
        return item
