"""adding content to posts table

Revision ID: 3fc7b835ad68
Revises: ea012a0de423
Create Date: 2022-12-19 21:01:58.009890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fc7b835ad68'
down_revision = 'ea012a0de423'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",sa.Column("content",sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column("posts")
    pass
