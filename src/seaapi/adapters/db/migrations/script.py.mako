"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
import os
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}
    script_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'sql', ${repr(up_revision)} + ".sql"))
    if os.path.exists(script_path):
        with open(script_path, "r") as f:
            script_content = f.read()

        conn = op.get_bind()
        if conn.dialect.name == 'sqlite':

            conn.connection.executescript(script_content)
        else:
            op.execute(script_content)


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}