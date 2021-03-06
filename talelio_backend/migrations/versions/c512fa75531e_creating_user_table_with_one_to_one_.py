"""creating user table with one-to-one account relation

Revision ID: c512fa75531e
Revises: c0147367a302
Create Date: 2021-03-23 11:59:02.905721

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c512fa75531e'
down_revision = 'c0147367a302'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'user', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('avatar_url', sa.String(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ['account_id'],
            ['account.id'],
        ), sa.PrimaryKeyConstraint('id'))
    op.add_column(
        'account',
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('account', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('account', sa.Column('verified', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('account', 'verified')
    op.drop_column('account', 'updated_at')
    op.drop_column('account', 'created_at')
    op.drop_table('user')
    # ### end Alembic commands ###
