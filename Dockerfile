FROM python:2-slim

COPY src /usr/src/app/

WORKDIR /usr/src/app

ENTRYPOINT ["python", "-u"]

CMD ["publisher.py"]
