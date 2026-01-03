"""
Procedury bazy SQL
1. AddCopy dodaje egzemplarz danego tytulu do tblMediaCopy:
    - Sprawdza czy tblMediaTitles zawiera dany MediaTitle
        - Jezeli zawiedzie, zaproponuje utworzenie nowego rekordu
            - Potrzebowac bedzie: MediaType, MediaGenre, MediaDate
            - W innym przypadku TitleNotRegistered ERROR

2. SellCopy rejestruje sprzedaz egzemplarza w tblSales:
    - Uzupelnia pole SalePrice o wartosc tblMediaCopies.CopyPrice
    - W przypadku nieistniejacego/nieaktywnego EmployeeID -> EmployeeNonExistent/EmployeeInactive ERROR
    - W przypadku, gdy tblMediaCopies.CopyStatus = SOLD -> Search for AVAILABLE -> Change tblSales.CopyID, else throw CopyAlreadySold ERROR
    - Na podstawie tblSales.CopyID, zaktualizuj tblMediaCopies.CopyStatus = SOLD
"""