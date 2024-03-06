FROM registry.gitlab.com/biglittletech/platform/packages/python-poetry:1.0.1

ARG HTTPS_PROXY

WORKDIR /code
COPY pyproject.toml poetry.loc[k] src /code/
RUN poetry install
RUN poetry build
RUN pip install dist/*.tar.gz

ENTRYPOINT [ "wait-for-it-mongo" ]
