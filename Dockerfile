FROM python:3.10.1-alpine3.15

WORKDIR /app

EXPOSE 5000

COPY key_server_app /app

RUN pip3 install -r requirements.txt

CMD [ "python3", "run_server.py"]
