FROM python:3.11-slim-bullseye
WORKDIR /app
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["python", "app.py"]