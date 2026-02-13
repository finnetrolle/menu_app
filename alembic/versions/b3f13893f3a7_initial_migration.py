"""Initial migration

Revision ID: b3f13893f3a7
Revises: 
Create Date: 2026-02-13 21:09:22.680754

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3f13893f3a7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create ingredients table
    op.create_table(
        'ingredients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('protein_g', sa.Float(), nullable=False),
        sa.Column('fat_g', sa.Float(), nullable=False),
        sa.Column('carbohydrates_g', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create dishes table
    op.create_table(
        'dishes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create dish_ingredients junction table
    op.create_table(
        'dish_ingredients',
        sa.Column('dish_id', sa.Integer(), nullable=False),
        sa.Column('ingredient_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['dish_id'], ['dishes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('dish_id', 'ingredient_id')
    )


def downgrade() -> None:
    op.drop_table('dish_ingredients')
    op.drop_table('dishes')
    op.drop_table('ingredients')
