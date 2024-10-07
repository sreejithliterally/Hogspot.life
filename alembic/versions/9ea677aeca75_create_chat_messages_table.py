"""Create chat_messages table

Revision ID: 9ea677aeca75
Revises: 82021fde5972
Create Date: 2024-10-07 07:20:37.1922

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = '9ea677aeca75'
down_revision: Union[str, None] = '82021fde5972'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the chat_messages table
    op.create_table(
        'chat_messages',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('sender_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('receiver_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('content', sa.String, nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=func.now(), nullable=False)
    )


def downgrade():
    # Drop the chat_messages table
    op.drop_table('chat_messages')
