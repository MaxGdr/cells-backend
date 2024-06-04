from typing import List
from sqlalchemy.orm import Session

from models.items import Item



class ItemsCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_items(self, skip: int = 0, limit: int = 100) -> List[Item]:
        items: List[Item] = self.db.query(Item).offset(skip).limit(limit).all()
        return items

    def create_item(self, item: Item) -> Item:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
