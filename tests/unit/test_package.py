from unittest import mock

import pytest

from npm_deps.error import PackageVersionNotFoundError
from npm_deps.package_version import get_package_version, resolve_dependencies

fake_npm_response = {
    "name": "some-package",
    "versions": {
        "0.0.9": {
            "dependencies": {},
            "name": "some-package",
            "version": "0.1.0",
        },
        "0.1.0": {
            "dependencies": {"other-package": "~1.0.5"},
            "name": "some-package",
            "version": "0.1.0",
        },
        "0.1.1": {
            "dependencies": {"other-package": "~1.0.5"},
            "name": "some-package",
            "version": "0.1.1",
        },
    },
    "other": "ignored fields",
}

fake_npm_response_no_dependencies = {
    "name": "some-package",
    "versions": {
        "0.0.8": {
            "dependencies": {},
            "name": "some-package",
            "version": "0.0.8",
        },
        "0.0.9": {
            "dependencies": {},
            "name": "some-package",
            "version": "0.0.9",
        },
    },
    "other": "ignored fields",
}

fake_npm_response_for_dependency_1 = {
    "name": "other-package",
    "versions": {
        "1.2.3": {
            "dependencies": {},
            "name": "other-package",
            "version": "1.2.3",
        },
        "1.2.4": {
            "dependencies": {},
            "name": "other-package",
            "version": "1.2.4",
        },
    },
    "other": "ignored fields",
}

fake_npm_response_for_dependency_2 = {
    "name": "another",
    "versions": {
        "2.0.1": {
            "dependencies": {},
            "name": "another",
            "version": "2.0.1",
        },
        "3.0.1": {
            "dependencies": {},
            "name": "another",
            "version": "3.0.1",
        },
    },
    "other": "ignored fields",
}


@pytest.mark.anyio
async def test_get_valid_package_version():
    with mock.patch("npm_deps.package_version.request_package") as mock_request_package:
        mock_request_package.return_value = fake_npm_response
        with mock.patch(
            "npm_deps.package_version.resolve_dependencies"
        ) as mock_resolve_dependencies:
            mock_resolve_dependencies.return_value = {"other-package": "1.0.5"}
            package_version_result = await get_package_version("some-package", "0.1.0")

    assert package_version_result.name == "some-package"
    assert package_version_result.version == "0.1.0"
    assert package_version_result.dependencies.get("other-package") == "1.0.5"
    mock_resolve_dependencies.assert_called_once()


@pytest.mark.anyio
async def test_get_package_version_without_dependencies():
    with mock.patch("npm_deps.package_version.request_package") as mock_request_package:
        with mock.patch(
            "npm_deps.package_version.resolve_dependencies"
        ) as mock_resolve_dependencies:
            mock_request_package.return_value = fake_npm_response_no_dependencies

        package_version_result = await get_package_version("some-package", "0.0.9")

    assert package_version_result.name == "some-package"
    assert package_version_result.version == "0.0.9"
    assert package_version_result.dependencies is None
    mock_resolve_dependencies.assert_not_called()


@pytest.mark.anyio
async def test_get_version_not_exists():
    with mock.patch("npm_deps.package_version.request_package") as mock_request_package:
        mock_request_package.return_value = fake_npm_response
        with pytest.raises(PackageVersionNotFoundError) as exception:
            await get_package_version("some-package", "9.9.9")
    assert exception.value.detail == "Package some-package version 9.9.9 not found"


@pytest.mark.anyio
async def test_resolves_dependencies():
    with mock.patch("npm_deps.package_version.request_package") as mock_request_package:
        mock_request_package.side_effect = [
            fake_npm_response_for_dependency_1,
            fake_npm_response_for_dependency_2,
        ]

        resolved_dependencies = await resolve_dependencies(
            {"other-package": "^1.2.3", "another": "^3.0.1"}
        )

    assert "other-package" in resolved_dependencies
    assert "another" in resolved_dependencies
    assert resolved_dependencies.get("other-package") == "1.2.4"
    assert resolved_dependencies.get("another") == "3.0.1"
