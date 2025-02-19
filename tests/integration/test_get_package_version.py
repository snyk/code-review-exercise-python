import json

import pytest
import requests_mock

from npm_deps.package import get_package_version


@pytest.mark.anyio
async def test_get_package_version_with_no_dependencies():
    with requests_mock.Mocker() as mock:
        with open("tests/integration/fixtures/aaa.json") as fp:
            data = json.load(fp)
            mock.get(
                "https://registry.npmjs.org/aaa",
                json=data,
            )
            package_version_response = await get_package_version("aaa", "0.0.2")

    assert package_version_response.name == "aaa"
    assert package_version_response.version == "0.0.2"
    assert package_version_response.dependencies is None


@pytest.mark.anyio
async def test_get_package_version_with_dependencies():
    with requests_mock.Mocker() as mock:
        with open("tests/integration/fixtures/a.json") as fp:
            data = json.load(fp)
            mock.get(
                "https://registry.npmjs.org/a",
                json=data,
            )
            with open("tests/integration/fixtures/a_mock.json") as fp:
                data = json.load(fp)
                mock.get(
                    "https://registry.npmjs.org/a_mock",
                    json=data,
                )
                with open("tests/integration/fixtures/a_mock.json") as fp:
                    data = json.load(fp)
                    mock.get(
                        "https://registry.npmjs.org/a_test",
                        json=data,
                    )
                    package_version_response = await get_package_version("a", "0.2.4")

    assert package_version_response.name == "a"
    assert package_version_response.version == "0.2.4"
    assert package_version_response.dependencies.get("a_mock") == "0.0.1"
    assert package_version_response.dependencies.get("a_test") == "0.0.2"
