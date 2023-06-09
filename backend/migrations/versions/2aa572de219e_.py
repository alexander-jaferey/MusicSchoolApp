"""empty message

Revision ID: 2aa572de219e
Revises: 4c20362cfce4
Create Date: 2023-05-03 10:37:37.781966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2aa572de219e'
down_revision = '4c20362cfce4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['name'])

    with op.batch_alter_table('instructors', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['first_name', 'last_name'])

    with op.batch_alter_table('instruments', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['instrument'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('instruments', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('instructors', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
