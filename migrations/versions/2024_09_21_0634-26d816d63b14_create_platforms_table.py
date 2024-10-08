"""create platforms table

Revision ID: 26d816d63b14
Revises: feeb33c5e5f5
Create Date: 2024-09-21 06:34:30.626024

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26d816d63b14'
down_revision: Union[str, None] = 'feeb33c5e5f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('platform',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.Column('client_id', sa.String(length=255), nullable=False),
    sa.Column('auth_login_url', sa.String(length=255), nullable=False),
    sa.Column('auth_token_url', sa.String(length=255), nullable=False),
    sa.Column('auth_audience', sa.String(length=255), nullable=True),
    sa.Column('key_set_url', sa.String(length=255), nullable=False),
    sa.Column('private_key_file', sa.String(length=255), nullable=False),
    sa.Column('public_key_file', sa.String(length=255), nullable=False),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('platform')
    # ### end Alembic commands ###
