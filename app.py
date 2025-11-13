from http import HTTPStatus

from fastapi import FastAPI
from starlette.responses import Response

from npm_deps.package import get_package

app = FastAPI(title="NpmDepsService", version="1.0")


@app.get("/healthcheck")
async def health() -> Response:
    return Response(status_code=HTTPStatus.NO_CONTENT)


@app.get("/package/{name}/{version}", tags=["package"])
async def get_package_version(name: str, version: str):  # type: ignore[no-untyped-def]
    return await get_package(name, version)
