"""
Sciezki do bazy danych
Tryb debugowy
Nazwa aplikacji
Wersja

np.
```
    from pathlib import Path

    APP_NAME = "StoreFlow"
    VERSION = "1.0.0"

    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    DATABASE_PATH = BASE_DIR / "database.db"

    DEBUG = True
```
"""