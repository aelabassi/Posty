"""create post table

Revision ID: d3f09133ad4c
Revises: 
Create Date: 2024-12-01 11:24:06.801187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3f09133ad4c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('title', sa.String),
        sa.Column('content', sa.String),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'))
    )


def downgrade() -> None:
    op.drop_table('posts')