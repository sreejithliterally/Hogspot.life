"""Add new fields to user table

Revision ID: 82021fde5972
Revises: c8debc31dc00
Create Date: 2024-09-24 18:31:27.575990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82021fde5972'
down_revision: Union[str, None] = 'c8debc31dc00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Add new fields to the users table
    op.add_column('users', sa.Column('education_level', sa.String(), nullable=True))
    op.add_column('users', sa.Column('college_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('profession', sa.String(), nullable=True))
    op.add_column('users', sa.Column('company', sa.String(), nullable=True))
    op.add_column('users', sa.Column('interests', sa.JSON(), nullable=True))  # Assuming you want to store a list of interests
    op.add_column('users', sa.Column('residence_location', sa.String(), nullable=True))
    op.add_column('users', sa.Column('workout_habits', sa.String(), nullable=True))
    op.add_column('users', sa.Column('drinking_habits', sa.String(), nullable=True))
    op.add_column('users', sa.Column('smoking_habits', sa.String(), nullable=True))
    op.add_column('users', sa.Column('height_cm', sa.Integer(), nullable=True))

    # Modify hotspots table (add a new field as an example)
    op.add_column('hotspots', sa.Column('new_field_example', sa.String(), nullable=True))


def downgrade():
    # Remove new fields from the users table
    op.drop_column('users', 'education_level')
    op.drop_column('users', 'college_name')
    op.drop_column('users', 'profession')
    op.drop_column('users', 'company')
    op.drop_column('users', 'interests')
    op.drop_column('users', 'residence_location')
    op.drop_column('users', 'workout_habits')
    op.drop_column('users', 'drinking_habits')
    op.drop_column('users', 'smoking_habits')
    op.drop_column('users', 'height_cm')

    # Remove example field from hotspots table
    op.drop_column('hotspots', 'new_field_example')
