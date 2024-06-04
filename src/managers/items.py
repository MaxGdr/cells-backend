from typing import List
from db.items import ItemsCrud
from models.items import Item
from schemas.items import ItemSchema
from sqlmodel import Session


class ItemsManager:
    def __init__(self, session: Session):
        self._items_crud = ItemsCrud()

    def get_items(self, skip: int = 0, limit: int = 100) -> List[ItemSchema]:
        db_items: List[Item] = self._items_crud.get_items(skip=0, limit=100)
        return [ItemSchema()._from_dto(item=item) for item in db_items]