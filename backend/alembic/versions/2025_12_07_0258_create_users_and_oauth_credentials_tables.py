"""create users and oauth_credentials tables

Revision ID: 2025_12_07_0258
Revises: 
Create Date: 2025-12-07 02:58:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2025_12_07_0258'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('google_user_id', sa.Text(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    op.create_index(op.f('ix_users_google_user_id'), 'users', ['google_user_id'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)

    # Create oauth_credentials table
    op.create_table(
        'oauth_credentials',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('provider', sa.String(length=50), nullable=False, server_default='google'),
        sa.Column('refresh_token', sa.Text(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('scopes', postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'provider')
    )


def downgrade() -> None:
    op.drop_table('oauth_credentials')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_google_user_id'), table_name='users')
    op.drop_table('users')

