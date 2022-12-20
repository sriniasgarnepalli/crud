"""add foriegn key to post table

Revision ID: f566c9cfd730
Revises: 3e721af86427
Create Date: 2022-12-19 22:21:55.515527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f566c9cfd730'
down_revision = '3e721af86427'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key("post_users_fk",source_table="posts",referent_table="credentials",local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")
    pass

def downgrade():
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column("posts","owner_id")
    pass
