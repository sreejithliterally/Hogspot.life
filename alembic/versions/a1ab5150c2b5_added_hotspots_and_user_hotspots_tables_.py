"""Added hotspots and user_hotspots tables and modified users and otps tables

Revision ID: a1ab5150c2b5
Revises: f1d37b858761
Create Date: 2024-05-26 13:00:09.825113

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = 'a1ab5150c2b5'
down_revision: Union[str, None] = 'f1d37b858761'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hotspots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('radius', sa.Float(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_hotspots_location', 'hotspots', ['location'], unique=False, postgresql_using='gist')
    op.create_index(op.f('ix_hotspots_id'), 'hotspots', ['id'], unique=False)
    op.create_index(op.f('ix_hotspots_name'), 'hotspots', ['name'], unique=False)
    op.create_table('user_hotspots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('hotspot_id', sa.Integer(), nullable=False),
    sa.Column('entered_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_seen_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['hotspot_id'], ['hotspots.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_hotspots_id'), 'user_hotspots', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_hotspots_id'), table_name='user_hotspots')
    op.drop_table('user_hotspots')
    op.drop_index(op.f('ix_hotspots_name'), table_name='hotspots')
    op.drop_index(op.f('ix_hotspots_id'), table_name='hotspots')
    op.drop_index('idx_hotspots_location', table_name='hotspots', postgresql_using='gist')
    op.drop_table('hotspots')
    # ### end Alembic commands ###