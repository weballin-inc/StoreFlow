"""
Procedury bazy SQL
    - sprawdz czy egzemplarz istnieje,
    - sprawdz czy jest dostepny,
    - zapisz sprzedaz,
    - zmien status kopii,
    - obsluz bledy.

Przyklad
```
    def sell_copy(copy_id, customer_id, employee_id):
        copy = repo.get_copy(copy_id)
        if copy.status == SOLD:
            raise CopyNotAvailableError()

        employee = repo.get_employee(employee_id)
        if employee.status != ACTIVE:
            raise EmployeeInactiveError()

        repo.create_sale(...)
        repo.update_copy_status(copy_id, SOLD)

```
"""