"""empty message

Revision ID: 65b5d6e9c262
Revises: 
Create Date: 2024-11-15 23:51:09.628242

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65b5d6e9c262'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('applicant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('birthday', sa.String(length=10), nullable=False),
    sa.Column('gender', sa.Integer(), nullable=False),
    sa.Column('experience', sa.Integer(), nullable=True),
    sa.Column('education', sa.String(length=15), nullable=True),
    sa.Column('citizen', sa.String(length=15), nullable=True),
    sa.Column('diplom', sa.String(length=15), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('enterprise',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('license', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('manager',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=50), nullable=False),
    sa.Column('telephone', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('gender', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vacancy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('enterprise_id', sa.Integer(), nullable=False),
    sa.Column('salary', sa.Integer(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('post', sa.String(length=50), nullable=False),
    sa.Column('education', sa.String(length=15), nullable=False),
    sa.Column('experience', sa.Integer(), nullable=False),
    sa.Column('citizen', sa.String(length=15), nullable=False),
    sa.ForeignKeyConstraint(['enterprise_id'], ['enterprise.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vacancy_id', sa.Integer(), nullable=False),
    sa.Column('applicant_id', sa.Integer(), nullable=False),
    sa.Column('manager_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['applicant_id'], ['applicant.id'], ),
    sa.ForeignKeyConstraint(['manager_id'], ['manager.id'], ),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancy.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('applicant_id'),
    sa.UniqueConstraint('manager_id'),
    sa.UniqueConstraint('vacancy_id')
    )
    op.create_table('request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('applicant_id', sa.Integer(), nullable=False),
    sa.Column('vacancy_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['applicant_id'], ['applicant.id'], ),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancy.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('applicant_id'),
    sa.UniqueConstraint('vacancy_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('request')
    op.drop_table('record')
    op.drop_table('vacancy')
    op.drop_table('manager')
    op.drop_table('enterprise')
    op.drop_table('applicant')
    # ### end Alembic commands ###
