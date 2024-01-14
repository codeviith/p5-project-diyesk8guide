"""empty message

Revision ID: 1dfd0206a61b
Revises: 
Create Date: 2024-01-13 18:40:15.103955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1dfd0206a61b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('_password_hash', sa.String(), nullable=False),
    sa.Column('fname', sa.String(), nullable=False),
    sa.Column('lname', sa.String(), nullable=False),
    sa.Column('rider_stance', sa.String(), nullable=False),
    sa.Column('boards_owned', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id')
    )
    op.create_table('boards',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('deck_type', sa.String(), nullable=False),
    sa.Column('deck_length', sa.String(), nullable=False),
    sa.Column('deck_material', sa.String(), nullable=False),
    sa.Column('truck_type', sa.String(), nullable=False),
    sa.Column('truck_width', sa.String(), nullable=False),
    sa.Column('controller_feature', sa.String(), nullable=False),
    sa.Column('controller_type', sa.String(), nullable=False),
    sa.Column('remote_feature', sa.String(), nullable=False),
    sa.Column('remote_type', sa.String(), nullable=False),
    sa.Column('motor_size', sa.String(), nullable=False),
    sa.Column('motor_kv', sa.String(), nullable=False),
    sa.Column('wheel_size', sa.String(), nullable=False),
    sa.Column('wheel_type', sa.String(), nullable=False),
    sa.Column('battery_voltage', sa.String(), nullable=False),
    sa.Column('battery_type', sa.String(), nullable=False),
    sa.Column('battery_capacity', sa.String(), nullable=False),
    sa.Column('battery_configuration', sa.String(), nullable=False),
    sa.Column('range_mileage', sa.String(), nullable=False),
    sa.Column('image_url', sa.String(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_boards_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_contacts_user_id_users')),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('gallery',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('image_filename', sa.String(), nullable=False),
    sa.Column('battery_series', sa.Integer(), nullable=False),
    sa.Column('battery_parallel', sa.Integer(), nullable=False),
    sa.Column('motor_type', sa.String(), nullable=False),
    sa.Column('wheel_type', sa.String(), nullable=False),
    sa.Column('truck_type', sa.String(), nullable=False),
    sa.Column('max_speed', sa.Integer(), nullable=False),
    sa.Column('hearts', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_gallery_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('gurus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_input', sa.String(), nullable=False),
    sa.Column('answer', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_gurus_user_id_users')),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('hearts',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('gallery_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['gallery_id'], ['gallery.id'], name=op.f('fk_hearts_gallery_id_gallery')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_hearts_user_id_users')),
    sa.PrimaryKeyConstraint('user_id', 'gallery_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hearts')
    op.drop_table('gurus')
    op.drop_table('gallery')
    op.drop_table('contacts')
    op.drop_table('boards')
    op.drop_table('users')
    # ### end Alembic commands ###
