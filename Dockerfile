FROM python:3.12.1-bookworm

LABEL org.opencontainers.image.source=https://github.com/fahadahammed/dummyapp
LABEL org.opencontainers.image.description="DummyApp to test in k8s and others."
LABEL org.opencontainers.image.licenses=MIT

RUN mkdir /opt/DummyApp
WORKDIR /opt/DummyApp

COPY app.py /opt/DummyApp
COPY requirements.txt /opt/DummyApp

RUN apt-get update && apt-get upgrade -y && apt-get install curl telnet -y

RUN pip install -r requirements.txt

CMD ["python3", "app.py"]