"""
1. (CREATE dla tblMediaCopies) 
    AddCopy dodaje egzemplarz danego tytulu do tblMediaCopy:
    - Sprawdza czy tblMediaTitles zawiera dany MediaTitle
        - Jezeli zawiedzie, zaproponuje utworzenie nowego rekordu
            - Potrzebowac bedzie: MediaType, MediaGenre, MediaDate
            - W innym przypadku TitleNotRegistered ERROR

2. (UPDATE dla tblMediaCopies)
    UpdateCopyPrice:
    - Przyjmuje wylacznie zmiane wartosci tblMediaCopies.CopyPrice
    - Aktualizuje wszystkie rekordy z tym samym tblMediaCopies.MediaID
        - Z wylaczeniem tych z CopyStatus = SOLD
"""

"""
1. (CREATE dla tblSales) 
    SellCopy rejestruje sprzedaz egzemplarza w tblSales:
    - tblSales.SaleDate = GETDATE()
    - Uzupelnia pole SalePrice o wartosc tblMediaCopies.CopyPrice
    - W przypadku nieistniejacego/nieaktywnego EmployeeID -> EmployeeNonExistent/EmployeeInactive ERROR
    - W przypadku, gdy tblMediaCopies.CopyStatus = SOLD -> Search for AVAILABLE -> Change tblSales.CopyID, else throw CopyAlreadySold ERROR
    - Na podstawie tblSales.CopyID, zaktualizuj tblMediaCopies.CopyStatus = SOLD
"""