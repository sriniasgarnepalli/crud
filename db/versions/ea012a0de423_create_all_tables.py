"""create all tables

Revision ID: ea012a0de423
Revises: 
Create Date: 2022-12-19 20:44:05.955664

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea012a0de423'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts",sa.Column("id",sa.Integer(),nullable=False,primary_key=True),sa.Column("title",sa.String(),nullable=False))
    pass

def downgrade():
    op.drop_table("posts")
    pass

# alembic revision -m "comment" this command will help us to create a version of db

# alembic upgrade revision this command will help us upgarde the tabels

# alembic revision --autogenerate This command will create a version with all the missing tables and columns from models file.