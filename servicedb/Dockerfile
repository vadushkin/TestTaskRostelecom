FROM python:3.10.4

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
COPY . /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install -r requirements.txt --compile --no-cache-dir

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
