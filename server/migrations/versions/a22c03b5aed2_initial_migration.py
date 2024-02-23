"""Initial migration

Revision ID: a22c03b5aed2
Revises: 
Create Date: 2024-02-22 14:11:56.720822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a22c03b5aed2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('card',
    sa.Column('card_type', sa.String(length=50), nullable=False),
    sa.Column('balance', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('interest_rate', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.PrimaryKeyConstraint('card_type')
    )
    op.create_table('employee',
    sa.Column('employee_id', sa.UUID(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('years_of_experience', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('employee_id'),
    sa.UniqueConstraint('employee_id')
    )
    op.create_table('transactions',
    sa.Column('transaction_id', sa.UUID(), nullable=False),
    sa.Column('transaction_date', sa.Date(), nullable=False),
    sa.Column('transaction_time', sa.Time(), nullable=False),
    sa.Column('vendor', sa.String(length=255), nullable=False),
    sa.Column('employee_id', sa.UUID(), nullable=False),
    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('location', sa.Text(), nullable=False),
    sa.Column('card_type', sa.String(length=50), nullable=False),
    sa.Column('transaction_type', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['card_type'], ['card.card_type'], ),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.employee_id'], ),
    sa.PrimaryKeyConstraint('transaction_id'),
    sa.UniqueConstraint('transaction_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions')
    op.drop_table('employee')
    op.drop_table('card')
    # ### end Alembic commands ###