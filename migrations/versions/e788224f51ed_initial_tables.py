"""Initial tables

Revision ID: e788224f51ed
Revises: 
Create Date: 2024-06-04 22:34:21.047178

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e788224f51ed'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('items',
        sa.Column('id', sa.Integer(), nullable=False, unique=True, index=True, primary_key=True),
        sa.Column('title', sa.String() , nullable=False, unique=True, index=True),
        sa.Column('description', sa.Text()),
        sa.Column('owner_id', sa.Integer()),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('items')
