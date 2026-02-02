from fastapi import HTTPException

def validate_range(
    field_name: str,
    value_from: int | float | None,
    value_to: int | float | None,
):
    if value_from is not None and value_to is not None and value_from > value_to:
        raise HTTPException(
            status_code=422,
            detail=f"{field_name}_from cannot be greater than {field_name}_to",
        )