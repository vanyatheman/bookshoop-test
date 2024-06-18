FROM python:3.9.19-slim-bookworm

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .

RUN apt update && apt install --no-install-recommends -y libpq-dev gcc python3-dev curl sudo
RUN pip install --upgrade pip \
    # && pip install 'gunicorn==20.1.0' \
    && pip install -r requirements.txt --no-cache-dir

COPY . .

RUN addgroup --system app && adduser --system --group app
RUN chown -R app:app /app
RUN chmod u+x /app/docker-start.sh

EXPOSE 8000


CMD ["/app/docker-start.sh"]
