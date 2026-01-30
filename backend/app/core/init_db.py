from app.core.database import get_connection


def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS tblMediaTitles (

            MediaID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            MediaType TEXT NOT NULL,
            ReleaseYear INTEGER NOT NULL,
            Publisher TEXT NOT NULL,

            UNIQUE(Title, MediaType)
        );


        CREATE TABLE IF NOT EXISTS tblMediaCopies (
        
            CopyID INTEGER PRIMARY KEY AUTOINCREMENT,
            MediaID INTEGER NOT NULL,
            Price REAL NOT NULL,
            Status TEXT NOT NULL,

            FOREIGN KEY (MediaID) REFERENCES tblMediaTitles(MediaID)
                ON DELETE RESTRICT
        );

        
        CREATE TABLE IF NOT EXISTS tblSales (
        
            SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
            CopyID INTEGER NOT NULL,
            Price REAL NOT NULL,
            
            FOREIGN KEY (CopyID) REFERENCES tblMediaCopies(CopyID)
                ON DELETE RESTRICT
        );
        """
    )

    conn.commit()
    conn.close()
