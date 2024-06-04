from typing import Any, List

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from models.items import Item, ItemCreate, ItemUpdate
from schemas.items import ItemSchema, ItemsGetRequestSchema, ItemsGetResponseSchema

from managers.items import ItemsManager
from deps import SessionDep

router = APIRouter()
items_manager = ItemsManager()


@router.get("/", response_model=ItemsGetResponseSchema)
def get_items(
    session: SessionDep, request: ItemsGetRequestSchema
) -> Any:
    """
    Retrieve items.
    """

    db_items: List[Item] = ItemsManager(session=session).get_items(skip=request.skip, limit=request.limit)
    return [ItemSchema()._from_dto(item=item) for item in db_items]

