from unittest import mock

import pytest

from npm_deps.package import get_package_version

fake_npm_response = {
    "name": "some_package",
    "description": "Some description",
    "dist-tags": {"latest": "0.1.0"},
    "versions": {
        "0.1.0": {
            "dependencies": {"lru-cache": "~1.0.5"},
            "name": "minimatch",
            "version": "0.1.1",
        }
    },
    "other": "ignored fields",
}


@pytest.mark.anyio
async def test_get_package_version():
    with mock.patch("npm_deps.package.request_package") as mock_request_package:
        mock_request_package.return_value = fake_npm_response
        result = await get_package_version("some_package", "0.1.0")
        assert result.name == "some_package"
        assert result.version == "0.1.0"
        assert result.dependencies.get("lru-cache") == "~1.0.5"
