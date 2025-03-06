FROM python:3.13.2-slim

WORKDIR /app

# Updates package lists, install packages, clean up package lists to reduce image size
RUN apt-get update && \
    apt-get install -y gcc python3-dev libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE ${BACKEND_PORT}

CMD ["python", "main.py"]
