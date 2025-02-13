from nodesemver import max_satisfying

from npm_deps.models import NPMPackage, NPMPackageVersion
from npm_deps.package_request import request_package


async def get_package_version(
    name: str, version: str | None = None
) -> NPMPackageVersion:

    # TODO: check Node and Golang versions for consistency on supporting on version: None
    package_json = await request_package(name)

    npm_package = NPMPackage(
        name=package_json.get("name"),
        versions=package_json.get("versions"),
    )

    if not version:
        version = max_satisfying(npm_package.versions.keys(), "*")

    dependencies = get_dependencies(npm_package, version)

    return NPMPackageVersion(
        name=name,
        version=version,
        dependencies=dependencies,
    )


def get_dependencies(npm_package, version) -> dict | None:
    if version:
        npm_package_version = npm_package.versions.get(version)
        if npm_package_version is not None:
            return dict(npm_package_version.dependencies)
    return None
