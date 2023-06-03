FROM python:3.9.13

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "train.py"]




