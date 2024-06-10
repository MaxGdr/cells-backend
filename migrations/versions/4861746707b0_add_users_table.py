"""Add users table

Revision ID: 4861746707b0
Revises: e788224f51ed
Create Date: 2024-06-06 23:42:11.976972

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4861746707b0'
down_revision: Union[str, None] = 'e788224f51ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False, unique=True, index=True, primary_key=True),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_foreign_key(
        constraint_name=None,
        source_table="items",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
    )


def downgrade() -> None:
    op.drop_table(
        'users'
    )
