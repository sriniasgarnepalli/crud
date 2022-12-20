"""add last few columns in posts table

Revision ID: 160331a63f4c
Revises: f566c9cfd730
Create Date: 2022-12-19 22:34:36.811023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '160331a63f4c'
down_revision = 'f566c9cfd730'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",sa.Column("published",sa.Boolean(),nullable=False,server_default="TRUE"),)
    op.add_column("posts",sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"),nullable=False),)
    pass


def downgrade():
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    pass
