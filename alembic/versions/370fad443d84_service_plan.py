"""service_plan

Revision ID: 370fad443d84
Revises: 1f39d0df0445
Create Date: 2024-07-24 17:19:42.689227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '370fad443d84'
down_revision = '1f39d0df0445'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contract',
    sa.Column('version', sa.String(length=20), nullable=False),
    sa.Column('document_uri', sa.String(), nullable=False),
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_contract_uuid'), 'contract', ['uuid'], unique=True)
    op.create_table('product',
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_product_uuid'), 'product', ['uuid'], unique=True)
    op.create_table('service_plan',
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('trial', sa.Boolean(), nullable=False),
    sa.Column('trial_days', sa.Integer(), nullable=True),
    sa.Column('contract_uuid', sa.Uuid(), nullable=False),
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['contract_uuid'], ['contract.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_service_plan_uuid'), 'service_plan', ['uuid'], unique=True)
    op.create_table('product_service_plan',
    sa.Column('product_uuid', sa.Uuid(), nullable=False),
    sa.Column('service_plan_uuid', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['product_uuid'], ['product.uuid'], ),
    sa.ForeignKeyConstraint(['service_plan_uuid'], ['service_plan.uuid'], ),
    sa.PrimaryKeyConstraint('product_uuid', 'service_plan_uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_service_plan')
    op.drop_index(op.f('ix_service_plan_uuid'), table_name='service_plan')
    op.drop_table('service_plan')
    op.drop_index(op.f('ix_product_uuid'), table_name='product')
    op.drop_table('product')
    op.drop_index(op.f('ix_contract_uuid'), table_name='contract')
    op.drop_table('contract')
    # ### end Alembic commands ###
