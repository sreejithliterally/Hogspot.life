"""add enum columns from users

Revision ID: 1e64b45a43ff
Revises: 5232e09cc982
Create Date: 2024-10-07 13:25:21.971386

"""
from typing import Sequence, Union
import enum


from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1e64b45a43ff'
down_revision: Union[str, None] = '5232e09cc982'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


class EducationLevel(enum.Enum):
    school = "school"
    college = "college"


class SmokingHabit(enum.Enum):
    occasionally = "occasionally"
    never = "never"
    socially = "socially"


class DrinkingHabit(enum.Enum):
    occasionally = "occasionally"
    never = "never"
    socially = "socially"


class WorkoutHabit(enum.Enum):
    daily = "daily"
    never = "never"
    sometimes = "sometimes"



def upgrade():
    # Adding new columns to the users table
    op.add_column('users', sa.Column('smoking', sa.Enum(SmokingHabit), nullable=True))
    op.add_column('users', sa.Column('drinking', sa.Enum(DrinkingHabit), nullable=True))
    op.add_column('users', sa.Column('workout', sa.Enum(WorkoutHabit), nullable=True))
    op.add_column('users', sa.Column('education_level', sa.Enum(EducationLevel), nullable=True))


def downgrade():
    # Dropping the added columns
    op.drop_column('users', 'smoking')
    op.drop_column('users', 'drinking')
    op.drop_column('users', 'workout')
    op.drop_column('users', 'interests')
    op.drop_column('users', 'education_level')
### end Alembic commands ###
