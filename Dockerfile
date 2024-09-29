FROM python:3.11 as build

RUN apt-get update && apt-get install -y build-essential curl
ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh
COPY ./requirements/prod.txt .
RUN /root/.cargo/bin/uv venv /opt/venv && \
    /root/.cargo/bin/uv pip install --no-cache -r prod.txt

FROM python:3.11-slim

COPY . /all-rag-tester
WORKDIR /all-rag-tester

COPY --from=build /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"
