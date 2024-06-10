"""models

Revision ID: f4b0b6b708db
Revises: 4861746707b0
Create Date: 2024-06-10 13:15:43.565250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f4b0b6b708db'
down_revision: Union[str, None] = '4861746707b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from db.database import Base


import enum
from sqlalchemy import Enum


class ModelVersion(Base):
    __tablename__ = "models_versions"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, index=True, unique=True)
    description = Column(String)
    endpoint_id = Column(String, unique=True)

    model_id = Column(Integer, ForeignKey("models.id"))


def upgrade() -> None:
    op.create_table('models',
        sa.Column('id', sa.Integer(), nullable=False, unique=True, index=True, primary_key=True),
        sa.Column('name', sa.String() , nullable=False, unique=True, index=True),
        sa.Column('description', sa.Text()),
        sa.Column('model_type', sa.Enum('image_detection', 'image_classification', 'text_classification', name='modeltype'), nullable=False),
        sa.Column('owner_id', sa.Integer()),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_foreign_key(
        constraint_name=None,
        source_table="models",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
    )

    op.create_table('model_versions',
        sa.Column('id', sa.Integer(), nullable=False, unique=True, index=True, primary_key=True),
        sa.Column('number', sa.String(), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('endpoint_id', sa.String()),
        sa.Column('model_id', sa.Integer()),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_foreign_key(
        constraint_name=None,
        source_table="model_versions",
        referent_table="models",
        local_cols=["model_id"],
        remote_cols=["id"],
    )

def downgrade() -> None:
    op.drop_table('model_versions')
    op.drop_table('models')
