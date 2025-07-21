FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR  /technews

COPY requirements.txt /technews/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /technews/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
