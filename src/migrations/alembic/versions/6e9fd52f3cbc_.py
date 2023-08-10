"""empty message

Revision ID: 6e9fd52f3cbc
Revises:
Create Date: 2023-05-30 21:28:01.364317

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6e9fd52f3cbc"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "customers",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("fname", sa.String(), nullable=True),
        sa.Column("lname", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("customers")
    # ### end Alembic commands ###