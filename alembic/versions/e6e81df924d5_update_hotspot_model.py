"""Update Hotspot model

Revision ID: e6e81df924d5
Revises: 3c7dc5fc2172
Create Date: 2024-06-08 19:21:24.251624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e6e81df924d5'
down_revision: Union[str, None] = 'a1ab5150c2b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    # Add coordinates column as an array of floats
    op.add_column('hotspots', sa.Column('coordinates', postgresql.ARRAY(sa.Float()), nullable=True))
    
    # Alter radius column to be nullable and set default to 500.0
    op.alter_column('hotspots', 'radius',
               existing_type=sa.Float(),
               nullable=True,
               server_default=sa.text('500.0'))

def downgrade():
    # Remove coordinates column
    op.drop_column('hotspots', 'coordinates')
    
    # Revert radius column to not nullable and remove default value
    op.alter_column('hotspots', 'radius',
               existing_type=sa.Float(),
               nullable=False,
               server_default=None)
