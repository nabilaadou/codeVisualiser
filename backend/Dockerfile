FROM python:3

RUN mkdir /diagram

WORKDIR /diagram

COPY requirements.txt /script

RUN pip install -r /script/requirements.txt

EXPOSE 8000

CMD ["fastapi", "dev", "server.py"]