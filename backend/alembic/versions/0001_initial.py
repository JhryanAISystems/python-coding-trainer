"""initial schema: attempts, solves, streak_days

Revision ID: 0001
Revises:
Create Date: 2026-08-17

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "attempts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("exercise_id", sa.String(length=64), nullable=False),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("mode", sa.String(length=16), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("total_tests", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("passed_tests", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("results_json", sa.JSON(), nullable=False),
        sa.Column("duration_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_attempts_exercise_id", "attempts", ["exercise_id"])
    op.create_index("ix_attempts_created_at", "attempts", ["created_at"])

    op.create_table(
        "solves",
        sa.Column("exercise_id", sa.String(length=64), primary_key=True),
        sa.Column("solved", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("first_solved_at", sa.DateTime(), nullable=True),
        sa.Column("times_attempted", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("times_passed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("hints_used", sa.Integer(), nullable=False, server_default="0"),
    )

    op.create_table(
        "streak_days",
        sa.Column("day", sa.Date(), primary_key=True),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("solves", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_table("streak_days")
    op.drop_table("solves")
    op.drop_index("ix_attempts_created_at", table_name="attempts")
    op.drop_index("ix_attempts_exercise_id", table_name="attempts")
    op.drop_table("attempts")
