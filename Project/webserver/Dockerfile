FROM python:3.9.13

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip -r requirements.txt

COPY server.py .

EXPOSE 8000

CMD ["python", "server.py"]
