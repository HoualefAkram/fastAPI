"""added content

Revision ID: ebee7c9b856f
Revises: 65c00c495b95
Create Date: 2024-08-14 18:31:09.531954

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ebee7c9b856f"
down_revision: Union[str, None] = "65c00c495b95"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
