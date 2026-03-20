"""initial schema"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("telegram_id"),
    )
    op.create_index(op.f("ix_users_telegram_id"), "users", ["telegram_id"], unique=False)

    niche_enum = sa.Enum("EDTECH", "FOODTECH", "ECOTECH", "GAMEDEV", "FINTECH", name="startupniche")
    status_enum = sa.Enum("NOT_STARTED", "ACTIVE", "WON", "LOST", name="gamestatus")
    niche_enum.create(op.get_bind(), checkfirst=True)
    status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "games",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("startup_name", sa.String(length=120), nullable=False),
        sa.Column("startup_niche", niche_enum, nullable=False),
        sa.Column("money", sa.Integer(), nullable=False),
        sa.Column("reputation", sa.Integer(), nullable=False),
        sa.Column("clients", sa.Integer(), nullable=False),
        sa.Column("product_level", sa.Integer(), nullable=False),
        sa.Column("team_level", sa.Integer(), nullable=False),
        sa.Column("marketing_level", sa.Integer(), nullable=False),
        sa.Column("turns", sa.Integer(), nullable=False),
        sa.Column("risk", sa.Integer(), nullable=False),
        sa.Column("current_day", sa.Integer(), nullable=False),
        sa.Column("game_status", status_enum, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index(op.f("ix_games_user_id"), "games", ["user_id"], unique=False)

    op.create_table(
        "upgrades",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("cost", sa.Integer(), nullable=False),
        sa.Column("money_bonus", sa.Integer(), nullable=False),
        sa.Column("reputation_bonus", sa.Integer(), nullable=False),
        sa.Column("clients_bonus", sa.Integer(), nullable=False),
        sa.Column("product_bonus", sa.Integer(), nullable=False),
        sa.Column("team_bonus", sa.Integer(), nullable=False),
        sa.Column("marketing_bonus", sa.Integer(), nullable=False),
        sa.Column("risk_bonus", sa.Integer(), nullable=False),
        sa.Column("one_time", sa.Boolean(), nullable=False),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "user_upgrades",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("game_id", sa.Integer(), sa.ForeignKey("games.id", ondelete="CASCADE"), nullable=False),
        sa.Column("upgrade_id", sa.Integer(), sa.ForeignKey("upgrades.id", ondelete="CASCADE"), nullable=False),
    )
    op.create_index(op.f("ix_user_upgrades_game_id"), "user_upgrades", ["game_id"], unique=False)
    op.create_index(op.f("ix_user_upgrades_upgrade_id"), "user_upgrades", ["upgrade_id"], unique=False)

    op.create_table(
        "game_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("startup_name", sa.String(length=120), nullable=False),
        sa.Column("niche", sa.String(length=50), nullable=False),
        sa.Column("final_day", sa.Integer(), nullable=False),
        sa.Column("final_money", sa.Integer(), nullable=False),
        sa.Column("final_reputation", sa.Integer(), nullable=False),
        sa.Column("final_clients", sa.Integer(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("outcome", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index(op.f("ix_game_results_score"), "game_results", ["score"], unique=False)
    op.create_index(op.f("ix_game_results_user_id"), "game_results", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_game_results_user_id"), table_name="game_results")
    op.drop_index(op.f("ix_game_results_score"), table_name="game_results")
    op.drop_table("game_results")
    op.drop_index(op.f("ix_user_upgrades_upgrade_id"), table_name="user_upgrades")
    op.drop_index(op.f("ix_user_upgrades_game_id"), table_name="user_upgrades")
    op.drop_table("user_upgrades")
    op.drop_table("upgrades")
    op.drop_index(op.f("ix_games_user_id"), table_name="games")
    op.drop_table("games")
    op.drop_index(op.f("ix_users_telegram_id"), table_name="users")
    op.drop_table("users")
