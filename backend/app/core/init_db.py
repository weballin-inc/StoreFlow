from app.core.database import get_connection


def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tblMediaTitles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            media_type TEXT NOT NULL,
            release_year INTEGER,
            publisher TEXT,
            UNIQUE(title, media_type)
        )
        """
    )

    conn.commit()
    conn.close()
