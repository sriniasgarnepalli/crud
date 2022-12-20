"""add user table

Revision ID: 3e721af86427
Revises: 3fc7b835ad68
Create Date: 2022-12-19 21:13:05.282475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e721af86427'
down_revision = '3fc7b835ad68'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("credentials",
                    sa.Column("id",sa.Integer(),nullable=False),
                    sa.Column("email",sa.String(),nullable=False),
                    sa.Column("password",sa.String(),nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"),nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email"))
    pass


def downgrade():
    op.drop_table("credentials")
    pass
