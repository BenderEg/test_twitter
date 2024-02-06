"""subscriptions

Revision ID: 85ec469f2794
Revises: 0e71bcd1b477
Create Date: 2024-02-06 15:24:01.126946

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85ec469f2794'
down_revision: Union[str, None] = '0e71bcd1b477'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscriptions',
    sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('subscriber_id', sa.Uuid(), nullable=False),
    sa.Column('creation_date', sa.TIMESTAMP(timezone=True), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['subscriber_id'], ['content.users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['content.users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'subscriber_id', name='user_subscriber_idx'),
    schema='content'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscriptions', schema='content')
    # ### end Alembic commands ###
