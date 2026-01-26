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

from app.domain.models import MediaTitle
from app.domain.enums import MediaType
from app.domain.exceptions import MediaAlreadyExistsError
from app.repositories import media_repo


def add_media_title(
    title: str,
    media_type: MediaType,
    release_year: int,
    publisher: str,
) -> MediaTitle:
    """
    Business procedure:
    - media title must be unique per (title, media_type)
    """

    existing = media_repo.get_by_title_and_type(title, media_type)
    if existing is not None:
        raise MediaAlreadyExistsError(
            f"Media '{title}' of type '{media_type.value}' already exists."
        )

    media = MediaTitle(
        id=None,
        title=title,
        media_type=media_type,
        release_year=release_year,
        publisher=publisher,
    )

    return media_repo.create(media)


def get_all_media_titles() -> list[MediaTitle]:
    """
    Returns all media titles.
    """
    return media_repo.get_all()
