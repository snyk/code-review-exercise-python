from npm_deps.models import NPMPackage, NPMPackageVersion
from npm_deps.package_request import request_package


async def get_package_version(name: str, version: str) -> NPMPackageVersion:

    package_json = await request_package(name)

    npm_package = NPMPackage(
        name=package_json.get("name"),
        versions=package_json.get("versions"),
    )

    dependencies = get_dependencies(npm_package, version)

    return NPMPackageVersion(
        name=name,
        version=version,
        dependencies=dependencies,
    )


def get_dependencies(npm_package, version) -> dict | None:
    npm_package_version = npm_package.versions.get(version)
    if npm_package_version is not None:
        return dict(npm_package_version.dependencies)
    return None
