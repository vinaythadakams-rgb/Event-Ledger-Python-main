from typing import Any

class DomainError(Exception):
    def __init__(self, message: str, details: Any | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details

class NotFoundError(DomainError):
    pass

class ConflictError(DomainError):
    pass

class ValidationError(DomainError):
    pass
