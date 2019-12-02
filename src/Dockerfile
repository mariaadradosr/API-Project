FROM python:3.7-slim

ADD . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

RUN adduser --disabled-password myuser
USER myuser 

CMD ["python3","-u","api.py"]