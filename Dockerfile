FROM python:3.12.3-alpine

COPY src /app/src
WORKDIR /app/src

COPY requirements.txt .
RUN pip install -r requirements.txt --use-pep517

EXPOSE 8000/tcp

ENTRYPOINT uvicorn ordermgmt.app:app --host 0.0.0.0 --port 8000