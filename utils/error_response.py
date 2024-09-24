from fastapi import HTTPException

class ErrorResponse(HTTPException):
    def __init__(self, status_code: int = 400, error_message: str = "An error occurred"):
        super().__init__(status_code=status_code, detail=error_message)
