FROM python:3.9 as builder

COPY . /project
WORKDIR /project

RUN pip install poetry
RUN poetry export --without-hashes -o requirements.txt -f requirements.txt
RUN poetry build --format=wheel
RUN cp dist/* /tmp
RUN pip wheel --no-cache-dir --disable-pip-version-check -r requirements.txt -w /tmp

FROM python:3.9-slim
COPY --from=builder /tmp /tmp
RUN pip install --no-cache-dir --disable-pip-version-check --no-index --no-deps /tmp/*.whl
COPY . /srv/project
WORKDIR /srv/project

RUN apt update && apt install -yq curl

CMD ["uvicorn", "--forwarded-allow-ips='*'", "--proxy-headers", "--host", "0.0.0.0", "keycloak_collective_portal.main:app"]
EXPOSE 8000
