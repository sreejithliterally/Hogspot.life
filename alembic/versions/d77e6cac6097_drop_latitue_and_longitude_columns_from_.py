"""drop latitue and longitude columns from hotspots

Revision ID: d77e6cac6097
Revises: e6e81df924d5
Create Date: 2024-06-08 19:38:50.350176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd77e6cac6097'
down_revision: Union[str, None] = 'e6e81df924d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Remove latitude and longitude columns
    op.drop_column('hotspots', 'latitude')
    op.drop_column('hotspots', 'longitude')


def downgrade():
    # Add latitude and longitude columns back
    op.add_column('hotspots', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('hotspots', sa.Column('longitude', sa.Float(), nullable=True))