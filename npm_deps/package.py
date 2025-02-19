from nodesemver import max_satisfying

from npm_deps.error import PackageVersionNotFoundError
from npm_deps.models import NPMPackage, NPMPackageVersion
from npm_deps.package_request import request_package


async def get_package_version(name: str, version: str) -> NPMPackageVersion:
    """
    Returns an NPM package with a given name and version
    with resolved direct dependencies.

    Keyword arguments:
    name -- the name of the package
    version -- version of the package
    """
    package_json = await request_package(name)

    npm_package = NPMPackage(
        name=package_json.get("name"),
        versions=package_json.get("versions"),
    )

    package_for_version = npm_package.versions.get(version)
    if package_for_version is None:
        raise PackageVersionNotFoundError(f"Package {name} version {version} not found")

    dependencies = (
        await resolve_dependencies(package_for_version.dependencies)
        if package_for_version.dependencies
        else None
    )

    return NPMPackageVersion(name=name, version=version, dependencies=dependencies)


async def resolve_dependencies(dependencies: dict) -> dict:
    """
    Returns the max satisfying version for each dependency.

    Keyword arguments:
    dependencies -- dictionary of package names with version ranges
    """
    resolved_dependencies = {}
    for dependency_name, dependency_range in dependencies.items():
        dependency_package_json = await request_package(dependency_name)
        dependency_versions = dependency_package_json.get("versions", {}).keys()
        max_satisfying_version = max_satisfying(dependency_versions, dependency_range)
        resolved_dependencies[dependency_name] = max_satisfying_version
    return resolved_dependencies
