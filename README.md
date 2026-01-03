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
  - Rejestrowanie pracowników.


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

#### Endpointy API
`PLACEHOLDER`

### Struktura bazy danych
Baza danych SQLite składa się z prostych tabel, a całość zawarta jest w pojedyńczym pliku `dabatase.db`, dzięki czemu możliwe jest tworzenie backupów i pełne formatowanie bazy danych bez potrzeby rozbierania kodu na czynniki pierwsze.

Struktura tabel jest relacyjna, gdzie głównymi kluczami są ID każdego z przedmiotów. Każdy fizyczny egzemplarz danego utworu stanowi oddzielny wiersz w odpowiedniej tabeli.

#### Tabele
- tblMediaTitles
    - MediaID (INTEGER) PRIMARY KEY
    - MediaTitle (NVARCHAR)
    - MediaType (VARCHAR)
    - MediaGenre (VARCHAR)
    - MediaDate (DATETIME)

- tblMediaCopies
    - CopyID (INTEGER) PRIMARY KEY
    - MediaID (INTEGER) FOREIGN KEY → tblMediaTitles(MediaID)
    - CopyStatus (VARCHAR)
    - CopyPrice (DECIMAL)

- tblSales
    - SaleID (INTEGER) PRIMARY KEY
    - CopyID (INTEGER) FOREIGN KEY → tblMediaCopies(CopyID)
    - SaleDate (DATETIME)
    - SalePrice (DECIMAL)
    - EmployeeID (INTEGER) FOREIGN KEY → tblEmployees(EmployeeID)

- tblEmployees
    - EmployeeID (INTEGER) PRIMARY KEY
    - EmployeeName (VARCHAR)
    - EmployeeGrade (VARCHAR)
    - EmployeeStatus (VARCHAR)

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