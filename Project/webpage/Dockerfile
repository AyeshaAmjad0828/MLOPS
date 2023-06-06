# Dockerfile-streamlit
FROM python:3.9.13

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
