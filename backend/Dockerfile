FROM python:3

RUN mkdir /backend

WORKDIR /backend

COPY requirements.txt /root/script/requirements.txt

RUN pip install -r /root/script/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]