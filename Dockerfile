
FROM python:3.9.13-slim

COPY requirements.txt /app/requirements.txt
COPY app/. /app

WORKDIR /app

RUN pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt
RUN flask db init
RUN flask db migrate
RUN flask db upgrade

ENTRYPOINT [ "python3" ]

CMD ["app.py" ]
