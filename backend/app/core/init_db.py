from app.core.database import get_connection


def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tblMediaTitles (

            MediaID INTEGER PRIMARY KEY AUTOINCREMENT,
            MediaTitle TEXT NOT NULL,
            MediaType TEXT NOT NULL,
            MediaReleaseYear INTEGER NOT NULL,
            MediaPublisher TEXT NOT NULL,

            UNIQUE(MediaTitle, MediaType)
        )
        """
    )

    conn.commit()
    conn.close()
