# pull official base image
FROM python:3.12.4-slim as builder

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# pull official base image
FROM python:3.12.4-slim

EXPOSE 8000

COPY --from=builder /opt/venv /opt/venv
# set work directory
WORKDIR /usr/src/app

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"
# copy project
COPY ./src .

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]