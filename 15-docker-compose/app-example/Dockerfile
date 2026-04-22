FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install flask

ENV ENV=prod

CMD ["python", "app.py"]
