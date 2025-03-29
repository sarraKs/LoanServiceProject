FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir grpcio grpcio-tools

CMD ["python3", "main.py"]
