"""
    Modele danych do komunikacji przez API

    Pydantic jest uzywany do walidacji danych
    ```
        from pydantic import BaseModel
        class CustomerCreate(BaseModel):
            copy_id:        int
            customer_id:    int
            employee_id:    int
    ```
    Dzieki czemu okreslajac typ danej zmiennej 
    jako ten w klasie
    mamy juz wgrany validator

    mozna rowniez dodawac validatory customowe
    ```
        from pydantic import validator
        class SaleCreate(BaseModel):
            price: float

            @validator("price")
            def check_price(this_class, value):
                if value <= 0
                    raise ValueError("price must be pos")
                return value
    ```
"""