from typing import List, Any, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.items import Item


class ItemsCrud:
    def __init__(self, db: Session):
        self._db = db

    async def get_items(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        items: Sequence[Any] = (
            self._db.scalars(
                select(Item).where(Item.owner_id == user_id).offset(skip).limit(limit)
            )
        ).all()
        return list(items)

    async def create_item(self, item: Item) -> Item:
        try:
            self._db.add(item)
            self._db.commit()
            self._db.refresh(item)
        except IntegrityError as exc:
            self._db.rollback()
            raise exc
        return item
