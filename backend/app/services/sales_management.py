"""
1. (CREATE dla tblSales) 
    SellCopy rejestruje sprzedaz egzemplarza w tblSales:
    - tblSales.SaleDate = GETDATE()
    - Uzupelnia pole SalePrice o wartosc tblMediaCopies.CopyPrice
    - W przypadku nieistniejacego/nieaktywnego EmployeeID -> EmployeeNonExistent/EmployeeInactive ERROR
    - W przypadku, gdy tblMediaCopies.CopyStatus = SOLD -> Search for AVAILABLE -> Change tblSales.CopyID, else throw CopyAlreadySold ERROR
    - Na podstawie tblSales.CopyID, zaktualizuj tblMediaCopies.CopyStatus = SOLD
"""