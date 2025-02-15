from http import HTTPStatus

from fastapi import HTTPException


class PackageVersionNotFoundError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(HTTPStatus.NOT_FOUND, detail)
