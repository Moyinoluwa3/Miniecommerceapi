"""empty message

Revision ID: 09f8f159508e
Revises: 65175bbf3bb6
Create Date: 2022-06-18 20:28:45.484494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09f8f159508e'
down_revision = '65175bbf3bb6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=True))
    op.execute("UPDATE users SET last_name = false")
    op.alter_column('users', 'last_name', nullable=False)

    pass


def downgrade() -> None:
    op.drop_column('users', 'last_name')
    pass
