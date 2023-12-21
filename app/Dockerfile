FROM python:3.10

RUN apt-get update && apt-get install -y bash

WORKDIR /app

COPY src /app/src
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

# Seu comando para iniciar a aplicação sem uvicorn
CMD ["python", "src/bot.py"]
