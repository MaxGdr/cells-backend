from typing import List
from db.items import ItemsCrud
from models.items import Item
from schemas.items import ItemSchema
from sqlalchemy.ext.asyncio import AsyncSession


class ItemsManager:
    def __init__(self, session: AsyncSession):
        self._items_crud = ItemsCrud(db=session)

    async def get_items(self, skip: int, limit: int) -> List[ItemSchema]:
        db_items: List[Item] = await self._items_crud.get_items(skip=skip, limit=limit)
        return [ItemSchema()._from_dto(item=item) for item in db_items]