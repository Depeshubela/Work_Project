ARG PYTHON_VERSION=3.10-slim-buster

FROM python:3.9.6-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt

RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE 8000
COPY function .



# replace demo.wsgi with <project_name>.wsgi
#CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "demo.wsgi"]
CMD ["/bin/bash", "-c", "python manage.py collectstatic --noinput; gunicorn --bind :8080 --workers 1 demo.wsgi"]