from npm_deps.error import PackageVersionNotFoundError
from npm_deps.models import NPMPackage, NPMPackageVersion
from npm_deps.package_request import request_package


async def get_package_version(name: str, version: str) -> NPMPackageVersion:

    package_json = await request_package(name)

    npm_package = NPMPackage(
        name=package_json.get("name"),
        versions=package_json.get("versions"),
    )

    package_version = npm_package.versions.get(version)
    if package_version is None:
        raise PackageVersionNotFoundError(f"Package {name} version {version} not found")

    return NPMPackageVersion(
        name=name,
        version=version,
        dependencies=package_version.dependencies,
    )
