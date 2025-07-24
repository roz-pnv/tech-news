FROM python:3.12-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --fix-missing \
    wget \
    curl \
    unzip \
    gnupg \
    fonts-liberation \
    libfontconfig1 \
    libxss1 \
    libappindicator1 \
    libnss3 \
    libasound2 \
    chromium \
    chromium-driver \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

WORKDIR /technews
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /technews/

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
