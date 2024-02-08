"""initial

Revision ID: 8742ef8b8a70
Revises:
Create Date: 2024-02-08 14:02:19.180563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import expression

# revision identifiers, used by Alembic.
revision: str = '8742ef8b8a70'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(expression.text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
    op.create_table('users',
    sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('creation_date', sa.TIMESTAMP(timezone=True), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('modified', sa.TIMESTAMP(timezone=True), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='content'
    )
    op.create_table('posts',
    sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('header', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('creation_date', sa.TIMESTAMP(timezone=True), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['content.users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='content'
    )
    op.create_index('user_id_idx', 'posts', ['user_id'], unique=False, schema='content')
    op.create_table('subscriptions',
    sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('subscriber_id', sa.Uuid(), nullable=False),
    sa.Column('creation_date', sa.TIMESTAMP(timezone=True), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['subscriber_id'], ['content.users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['content.users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'subscriber_id', name='user_subscriber_idx'),
    schema='content'
    )
    op.create_table('feeds',
    sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('author_id', sa.Uuid(), nullable=False),
    sa.Column('post_id', sa.Uuid(), nullable=False),
    sa.Column('header', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('creation_date', sa.TIMESTAMP(timezone=True), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('read', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['content.users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['post_id'], ['content.posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['content.users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'id'),
    schema='content',
    postgresql_partition_by='HASH (user_id)'
    )
    op.create_index('creation_date_idx', 'feeds', ['creation_date'], unique=False, schema='content')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('creation_date_idx', table_name='feeds', schema='content')
    op.drop_table('feeds', schema='content')
    op.drop_table('subscriptions', schema='content')
    op.drop_index('user_id_idx', table_name='posts', schema='content')
    op.drop_table('posts', schema='content')
    op.drop_table('users', schema='content')
    # ### end Alembic commands ###
