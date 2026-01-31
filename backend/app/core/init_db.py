from app.core.database import get_connection


def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS tblMedia (

            MediaID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            MediaType TEXT NOT NULL,
            ReleaseYear INTEGER NOT NULL,
            Publisher TEXT NOT NULL,
            Amount INTEGER NOT NULL,
            Price REAL NOT NULL,

            UNIQUE(Title, MediaType)
        );

        
        CREATE TABLE IF NOT EXISTS tblSales (
        
            SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
            MediaID INTEGER NOT NULL,
            Price REAL NOT NULL,
            Date DATETIME NOT NULL,
            
            FOREIGN KEY (MediaID) REFERENCES tblMedia(MediaID)
                ON DELETE RESTRICT
        );
        """
    )

    conn.commit()
    conn.close()
