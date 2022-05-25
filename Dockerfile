FROM ubuntu

RUN apt-get update -y && apt-get upgrade -y

RUN apt-get install python3 -y

RUN apt-get install python3-pip -y

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 9090

CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--port=9090", "--reload"]



