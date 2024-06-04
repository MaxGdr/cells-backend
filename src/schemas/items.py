from pydantic import BaseModel
from models.items import Item

class ItemSchema(BaseModel):
    id: int = None
    title: str
    owner_id: int

    def _from_dto(self, item: Item):
        self.id = item.id
        self.name = item.title
        self.owner_id = item.owner_id

    def _to_dto(self) -> Item:
        return Item(
            id=self.id,
            title=self.title,
            owner_id=self.owner_id
        )

class ItemsGetRequestSchema(BaseModel):
    skip: int = 0
    limit: int = 100

class ItemsGetResponseSchema(BaseModel):
    data: list[ItemSchema]
    count: int
