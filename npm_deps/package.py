import requests
from nodesemver import min_satisfying

from npm_deps.models import VersionedPackage
from npm_deps.package_request import request_package


async def get_package(name: str, range: str | None = "*") -> VersionedPackage:
    package_json = requests.get(f"https://registry.npmjs.org/{name}").json()
    versions = list(package_json["versions"].keys())
    version = min_satisfying(versions, range)
    version_record = package_json["versions"][version]

    package = VersionedPackage(
        name=package_json["name"],
        version=version_record["version"],
    )
    dependencies = version_record.get("dependencies", {})
    package.dependencies = [
        await get_package(name, version) for name, version in dependencies.items()
    ]
    return package


async def get_package_version(name: str, range: str) -> VersionedPackage:
    package_json = await request_package(name)
    versions = list(package_json["versions"].keys())
    version = min_satisfying(versions, range)
    deps_list = []
    for d in package_json["dependencies"]:
        package = VersionedPackage(name=d, version=package_json["dependencies"][d])
        deps_list.append(package)
    return VersionedPackage(
        name=name,
        version=version,
        dependencies=deps_list,
    )
