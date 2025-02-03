FROM python:3.13-slim
RUN apt-get update --no-install-recommends && \
    apt-get install --no-install-recommends -y dumb-init && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

RUN mkdir -p /srv/app && \
    mkdir -p /home/snyk

RUN addgroup --gid 1001 snyk
RUN useradd --gid 1001 --uid 1001 -s /bin/bash snyk && \
    chown -R snyk:snyk /home/snyk

RUN pip install --upgrade pip
RUN pip install poetry==2.0

RUN chown -R snyk:snyk /srv/app
USER snyk

WORKDIR /srv/app

# We add deps only first for improved docker caching
ADD pyproject.toml poetry.lock ./

ARG MODE
RUN if [ "$MODE" = "development" ]; then \
    printf "\e[35m\e[1m%s\e[0m\n" "WARNING: Installing in DEVELOPMENT mode"; \
    poetry install; \
    else \
    poetry install --without dev; \
    fi

ADD --chown=snyk:snyk . /srv/app/

CMD ["poetry", "run", "uvicorn", "app:app", "--host=0.0.0.0", "--port=3000", "--log-level=info"]
