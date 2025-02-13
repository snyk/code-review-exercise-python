from http import HTTPStatus

import pytest
import responses
from fastapi import HTTPException

from npm_deps.package_request import request_package


@responses.activate
@pytest.mark.anyio
async def test_request_package_exists():
    responses.add(
        responses.GET,
        "https://registry.npmjs.org/some_package",
        status=HTTPStatus.OK,
        json={"key1": "value1"},
    )

    result = await request_package("some_package")
    assert result == {"key1": "value1"}


@responses.activate
@pytest.mark.anyio
async def test_request_package_not_found():
    responses.add(
        responses.GET,
        "https://registry.npmjs.org/not_exists",
        status=HTTPStatus.NOT_FOUND,
    )
    with pytest.raises(HTTPException):
        await request_package("not_exists")


# TODO: add test for 500 error
