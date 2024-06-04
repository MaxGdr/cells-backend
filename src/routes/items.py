from typing import Any, List

from fastapi import APIRouter

from models.items import Item
from schemas.items import ItemSchema, ItemsGetRequestSchema, ItemsGetResponseSchema

from managers.items import ItemsManager
from deps import DBSessionDep

router = APIRouter()


@router.get("/", response_model=ItemsGetResponseSchema)
async def get_items(
    session: DBSessionDep, skip: int = 0, limit: int = 100,
) -> Any:
    """
    Retrieve items.
    """

    db_items: List[Item] = await ItemsManager(session=session).get_items(skip=skip, limit=limit)
    return ItemsGetResponseSchema(
        data=[ItemSchema()._from_dto(item=item) for item in db_items],
        count=len(db_items),
    )

