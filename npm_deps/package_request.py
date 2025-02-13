import logging
from http import HTTPStatus

import requests
from fastapi import HTTPException

NPM_REGISTRY_URL = "https://registry.npmjs.org"

logger = logging.getLogger(__name__)


async def request_package(name: str) -> dict:
    response = requests.get(f"{NPM_REGISTRY_URL}/{name}")
    logger.info("Status: %s", response.status_code)
    if response.status_code != HTTPStatus.OK:
        logger.error("Package: %s not found", name)
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to request package: {name} with status: {response.status_code}",
        )
    # TODO: define a domain type to return
    return response.json()  # type: ignore[no-any-return]
