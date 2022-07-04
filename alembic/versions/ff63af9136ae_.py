"""empty message

Revision ID: ff63af9136ae
Revises: 09f8f159508e
Create Date: 2022-06-18 20:33:10.750121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff63af9136ae'
down_revision = '09f8f159508e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('gender', sa.String(), nullable=True))
    op.execute("UPDATE users SET gender = false")
    op.alter_column('users', 'gender', nullable=False)
    pass


def downgrade() -> None:
    pass
