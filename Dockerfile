FROM ubuntu:latest

RUN apt update
RUN apt install python3 -y
RUN mkdir -p /app/src

WORKDIR /app/src

COPY . .

CMD [ "python3", "./bowling.py"]