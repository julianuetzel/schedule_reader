FROM python:3.10-slim as builder

RUN apt-get update -y \
    && apt-get install -y \
    && apt-get clean

COPY ./requirements.txt /app/requirements.txt
COPY ./src/config /app/config

RUN pip install --user -r /app/requirements.txt

RUN mkdir -p /app/

COPY src /app/src

FROM python:3.10-slim as app

RUN apt-get update -y \
    && apt-get install -y \
    && apt-get clean

COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app:$PYTHONPATH
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /app/src
ENTRYPOINT ["python", "main.py"]