from typing import Any, List

from fastapi import APIRouter

from models.items import Item
from schemas.items import ItemSchema, ItemsGetRequestSchema, ItemsGetResponseSchema

from managers.items import ItemsManager
from deps import SessionDep

router = APIRouter()


@router.get("/", response_model=ItemsGetResponseSchema)
def get_items(
    session: SessionDep, request: ItemsGetRequestSchema
) -> Any:
    """
    Retrieve items.
    """

    db_items: List[Item] = ItemsManager(session=session).get_items(skip=request.skip, limit=request.limit)
    return [ItemSchema()._from_dto(item=item) for item in db_items]

