from typing import List
from pydantic import BaseModel
from models.items import Item


class ItemSchema(BaseModel):
    id: int | None = None
    title: str
    owner_id: int

    @staticmethod
    def _from_dto(item: Item):  # type: ignore
        return ItemSchema(id=item.id, title=item.title, owner_id=item.owner_id)

    def _to_dto(self) -> Item:
        return Item(id=self.id, title=self.title, owner_id=self.owner_id)


class ItemsGetRequestSchema(BaseModel):
    skip: int = 0
    limit: int = 100


class ItemsGetResponseSchema(BaseModel):
    data: List[ItemSchema]
    count: int


class ItemsCreateRequestSchema(BaseModel):
    title: str
    owner_id: int


class ItemsCreateResponseSchema(BaseModel):
    data: ItemSchema
