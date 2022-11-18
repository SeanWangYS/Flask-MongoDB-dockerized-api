FROM python:3.9
WORKDIR /app
COPY data /app
COPY model /app
COPY app.py /app
COPY mongoDB.py /app
COPY requirements.txt /app
COPY hello.py /app
RUN pip install -r requirements.txt
# CMD ["python", "./app.py"]