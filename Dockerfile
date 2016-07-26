FROM python:2-slim

MAINTAINER aldwinb

WORKDIR /usr/src/app

COPY ["src", "requirements.txt", "/usr/src/app/"]

RUN pip install --upgrade -r requirements.txt

ENTRYPOINT ["python", "-u", "publisher.py"]
