from typing import Any, List

from fastapi import APIRouter

from schemas.items import (
    ItemSchema,
    ItemsGetResponseSchema,
    ItemsCreateRequestSchema,
    ItemsCreateResponseSchema,
)

from managers.items import ItemsManager
from deps import DBSessionDep

router = APIRouter()


@router.get("/", response_model=ItemsGetResponseSchema)
async def get_items(
    session: DBSessionDep,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve items.
    """

    items: List[ItemSchema] = await ItemsManager(session=session).get(
        skip=skip, limit=limit
    )
    print([item for item in items])

    return ItemsGetResponseSchema(
        data=items,
        count=len(items),
    )


@router.post("/", response_model=ItemsCreateResponseSchema)
async def create_item(
    session: DBSessionDep,
    item_request: ItemsCreateRequestSchema,
) -> Any:
    """
    Create an item.
    """

    item: ItemSchema = await ItemsManager(session=session).create(
        item=ItemSchema(title=item_request.title, owner_id=item_request.owner_id)
    )
    return ItemsCreateResponseSchema(data=item)
