from pydantic.v1 import BaseModel


class VersionedPackage(BaseModel):
    name: str
    version: str
    dependencies: list["VersionedPackage"] | None = None


class NPMPackageVersion(BaseModel):
    name: str
    version: str
    dependencies: dict[str, str] | None = None


class NPMPackage(BaseModel):
    name: str
    versions: dict[str, NPMPackageVersion]


VersionedPackage.update_forward_refs()
