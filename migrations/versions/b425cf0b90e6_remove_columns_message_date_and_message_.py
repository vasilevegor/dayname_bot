"""remove columns message_date and message_time, add message_datetime

Revision ID: b425cf0b90e6
Revises: 80d89ccca571
Create Date: 2023-08-21 02:49:13.919313

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "b425cf0b90e6"
down_revision: Union[str, None] = "80d89ccca571"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "chats", sa.Column("message_datetime", sa.DateTime(), nullable=True)
    )
    op.drop_column("chats", "message_time")
    op.drop_column("chats", "message_date")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "chats",
        sa.Column(
            "message_date", sa.DATE(), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "chats",
        sa.Column(
            "message_time", sa.DATE(), autoincrement=False, nullable=True
        ),
    )
    op.drop_column("chats", "message_datetime")
    # ### end Alembic commands ###