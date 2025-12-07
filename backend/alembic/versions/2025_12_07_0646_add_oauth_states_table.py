"""add oauth_states table

Revision ID: 2025_12_07_0646
Revises: 2025_12_07_0258
Create Date: 2025-12-07 06:46:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2025_12_07_0646'
down_revision = '2025_12_07_0258'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create oauth_states table for CSRF protection
    op.create_table(
        'oauth_states',
        sa.Column('state_token', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('state_token')
    )
    op.create_index(op.f('ix_oauth_states_created_at'), 'oauth_states', ['created_at'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_oauth_states_created_at'), table_name='oauth_states')
    op.drop_table('oauth_states')
