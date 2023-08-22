"""unique nickname

Revision ID: 38d097f3c351
Revises: 328289d9d1c0
Create Date: 2023-08-20 16:02:34.994904

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "38d097f3c351"
down_revision: Union[str, None] = "328289d9d1c0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "chats", ["nickname"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "chats", type_="unique")
    # ### end Alembic commands ###