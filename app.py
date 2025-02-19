from http import HTTPStatus

from fastapi import FastAPI
from starlette.responses import Response

from npm_deps.models import NPMPackageVersion
from npm_deps.package_version import get_package_version

app = FastAPI(title="NpmDepsService", version="1.0")


@app.get("/healthcheck")
async def health() -> Response:
    return Response(status_code=HTTPStatus.NO_CONTENT)


@app.get("/package/{name}/{version}", tags=["package"])
async def get_package(name: str, version: str) -> NPMPackageVersion:
    return await get_package_version(name, version)
