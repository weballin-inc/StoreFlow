# StoreFlow - Dokumentacja

## Czym jest StoreFlow?
StoreFlow to aplikacja desktopowa (Windows) do zarządzania sprzedażą nośników multimedialnych. System pozwala na kontrolę dostępności egzemplarzy, rejestrację transakcji oraz przegląd historii operacji w celu uporządkowania pracy danego punktu sprzedaży. 

Rodzaj nośników multimedialnych można dostosować wedle upodobań: czy są to książki, filmy, muzyka, czy gry komputerowe - struktura bazy danych jest na tyle prosta, że akceptuje dowolne rodzaje mediów.

### Funkcjonalności
- Architektura klient-serwer pozwalająca na edycję GUI bez potrzeby przepisywania logiki biznesowej.
- Prosty interfejs graficzny umożliwiający obsługę systemu bez kontaktu z SQL:
  - Dodawanie i edycja tytułów mediów w bazie danych.
  - Przeglądanie aktualnego stanu magazynu.
  - Rekordy poszczególnych egzemplarzy danego tytułu.
  - Realizacja sprzedaży egzemplarzy wraz z automatyczną zmianą ich statusu.
  - Zapisywanie historii transakcji sprzedaży.

## Architektura systemu
Aplikacja została podzielna na trzy elementy:
- Frontend (Desktop GUI)
- Backend (Logic and API)
- Baza danych (SQLite)

### Frontend (Desktop GUI)
Frontem aplikacji jest prosty interfejs graficzny pozwalający manipulować danymi z bazy danych bez potrzeby użycia SQL. Pomaga to nie tylko w zakresie dostępności dla niezaawansowanych użytkowników, ale również zapobiega potencjalnym problemom i błędom, które narażają dane na skasowanie.

#### Funkcjonalność GUI
`PLACEHOLDER`

### Backend (Logika i API)
Cała logika programu skupiająca się na modyfikacji i odczycie danych z bazy, oraz możliwości sporządzania raportów czy filtrowania wyników wyszukiwania.

Z racji tego, że niektóre operacje na bazie danych mają być wykonywane automatycznie (jak zmiana statusu przedmiotu po zarejestrowaniu sprzedaży), to w logice zawarte są również odpowiedniki procedur składowych.

W backendzie zawarte jest również API, dzięki czemu frontend otrzymuje wyłącznie endpointy do wykorzystania - zapewnia to łatwy rozwój aplikacji czy zmiany konfiguracji.

Projekt ogranicza zakres operacji modyfikujących dane do tych, które są logicznie uzasadnione w kontekście biznesowym systemu. Przykładowo, rekordy sprzedaży nie podlegają edycji, ponieważ wszystkie ich parametry są ustalane jednorazowo w momencie realizacji transakcji.

Podobnie operacje `POST /media` oraz `POST /sales` mają konkretne zasady zgodne z logiką biznesową.

#### Endpointy API
| Type of operation                              | API endpoint                     | Description                                                                                                                                                                                                                                                                                                         |
| ---------------------------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Create a Media record                          | `POST /media`                    | Create media record(s) with specified columns.<br><br>**Constraints:**<br>- Title **MUST** be provided<br>- MediaType **MUST** be in `{BOOK, GAME, MOVIE}`<br>- ReleaseYear **MUST** be `> 0`<br>- Publisher **MUST** be provided<br>- quantity **MUST** be `>= 0`<br>- Price **MUST** be `>= 0`                       |
| List all Media records (filtered)              | `GET /media`                     | List all media records that fulfill the provided filters. Every field can be used as a filter.                                                                                                                                                                                                                      |
| Edit a specific Media record (specific fields) | `PUT /media/{media_id}`          | Edit specific fields of the media record with given `media_id`.<br><br>**Editable fields:**<br>- Title<br>- MediaType (constraint: `Title + MediaType` must be unique)<br>- ReleaseYear<br>- Publisher<br>- Quantity (constraint: cannot be `< 0`)<br>- Price (constraint: cannot be `< 0`) |
| Modify quantity (inventory correction)         | `PATCH /media/{media_id}/{field}`| Modify media stock quantity/price using delta value.<br><br>**Rules:**<br>- Positive `quantity` → `quantity += quantity`<br>- Negative `quantity` → `quantity -= quantity`<br>- Resulting `quantity`, `price` **MUST** be `>= 0`                                                                                                                   |
| Delete Media record                            | —                                | **DELETE RESTRICTED**.<br>Rows can only be removed directly from the database using an appropriate SQL statement.                                                                                                                                                                                                   |
| Create a Sale record                           | `POST /sales/{media_id}`         | Create a sale record for the given `media_id`.<br><br>**Process:**<br>- `tblMedia.quantity` is reduced by `1`<br>- `rowcount` check ensures `quantity > 0` and valid `MediaID`<br>- All operations are executed within a **single database transaction**<br><br>**Automatically filled fields:**<br>- Price is taken from `tblMedia.Price` (snapshot)<br>- Date is taken from `datetime` package|
| List all Sale records (filtered)               | `GET /sales`                     | List all sale records with joined `tblMedia` data. Can be filtered by date range and `MediaID`.                                                                                                                                                                                                                                                                                                 |
| Update Sale record                             | —                                | **UPDATE RESTRICTED**.<br>Sale records are immutable and cannot be modified.                                                                                                                                                                                                                                                                                                                    |
| Delete Sale record                             | —                                | **DELETE RESTRICTED**.<br>Sale records cannot be removed to preserve sales history.                                                                                                                                                                                                                                                                                                             |


### Struktura bazy danych
Baza danych SQLite składa się z prostych tabel, a całość zawarta jest w pojedyńczym pliku `dabatase.db`, dzięki czemu możliwe jest tworzenie backupów i pełne formatowanie bazy danych bez potrzeby rozbierania kodu na czynniki pierwsze.

Struktura tabel jest relacyjna, gdzie głównymi kluczami są ID każdego z przedmiotów. Każdy fizyczny egzemplarz danego utworu stanowi oddzielny wiersz w odpowiedniej tabeli.

#### Tabele
- tblMedia
    - MediaID (INTEGER) PRIMARY KEY
    - Title (TEXT)
    - MediaType (TEXT)
    - ReleaseYear (DATE)
    - Publisher (TEXT)
    - quantity (INTEGER)
    - Price (REAL)

- tblSales
    - SaleID (INTEGER) PRIMARY KEY
    - MediaID (INTEGER) FOREIGN KEY → tblMedia(MediaID)
    - Price (REAL)
    - Date (DATETIME)

### Technologie
Użyte narzędzia i biblioteki dostępne są również w pliku `requirements.txt`
- `Python` (3.13)
- `FastAPI`
- `SQLite`
- `PySimpleGUI`
- `PLACEHOLDER`

## Instalacja i uruchomienie
`Releases`

### Instrukcja użytkownika
`PLACEHOLDER`