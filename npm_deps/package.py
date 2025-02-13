from nodesemver import max_satisfying

from npm_deps.models import NPMPackage, NPMPackageVersion
from npm_deps.package_request import request_package


async def get_package_version(
    name: str, version: str | None = None
) -> NPMPackageVersion:

    package_json = await request_package(name)

    npm_package = NPMPackage(
        name=package_json["name"],
        description=package_json["description"],
        dist_tags=package_json["dist-tags"],
        versions=package_json["versions"],
    )

    if not version:
        version = max_satisfying(npm_package.versions.keys(), "*")

    dependencies = (
        resolved_version.dependencies
        if version and (resolved_version := npm_package.versions.get(version))
        else None
    )
    return NPMPackageVersion(
        name=name,
        version=version,
        dependencies=dependencies,
    )
