"""init

Revision ID: 00c7f2948078
Revises: 0c3f4fdb1b91
Create Date: 2023-08-19 22:07:07.464022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00c7f2948078'
down_revision: Union[str, None] = '0c3f4fdb1b91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('chats', 'nickname',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)
    op.create_unique_constraint(None, 'chats', ['id'])
    op.create_unique_constraint(None, 'users', ['user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'chats', type_='unique')
    op.alter_column('chats', 'nickname',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
    # ### end Alembic commands ###
