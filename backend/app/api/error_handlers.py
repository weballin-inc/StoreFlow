"""
```
@app.exception_handler(CopyNotAvailableError)
async def handle_copy_error(request, exc):
    return JSONResponse(status_code=400, content={"error": "Copy not available"})
```
"""