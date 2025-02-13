from pydantic import BaseModel


class NPMPackageVersion(BaseModel):
    name: str
    version: str
    dependencies: dict[str, str] | None = None


class NPMPackage(BaseModel):
    name: str
    versions: dict[str, NPMPackageVersion]
