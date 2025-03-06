FROM python:3.9-slim

WORKDIR /app

# Install system dependencies required for MariaDB connector
# TODO: simplify and understand this
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# TODO: be most specific here
COPY . .

EXPOSE ${BACKEND_PORT}

CMD ["./run.sh"]
