##################### build stage #####################
FROM python:3.12-slim AS builder

# 🔧 system packages required to compile cryptography
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
##################### runtime stage ###################
#FROM python:3.12-slim
#
## same unprivileged user section you already have …
#RUN addgroup --system app && adduser --system --ingroup app app
WORKDIR /app
#COPY --from=builder /usr/local /usr/local
#COPY --from=builder /app /app
#USER app

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
