FROM python:3.8-slim-buster

WORKDIR /app

RUN pip install -r requirements.txt

COPY [".env", "main.py", "/app"]

ENTRYPOINT [ "python" ]

CMD ["main.py" ]