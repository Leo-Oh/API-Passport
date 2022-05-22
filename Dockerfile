FROM python:3.9.7

COPY ./src /app/src
COPY ./requirements.txt /app/

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 9090
  
CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--port=9090", "--reload"]
