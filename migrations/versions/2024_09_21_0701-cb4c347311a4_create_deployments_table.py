"""create deployments table

Revision ID: cb4c347311a4
Revises: 26d816d63b14
Create Date: 2024-09-21 07:01:31.179060

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb4c347311a4'
down_revision: Union[str, None] = '26d816d63b14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deployment',
    sa.Column('platform_id', sa.Integer(), nullable=False),
    sa.Column('deployment_id', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['platform_id'], ['platform.id'], ),
    sa.PrimaryKeyConstraint('platform_id', 'deployment_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deployment')
    # ### end Alembic commands ###