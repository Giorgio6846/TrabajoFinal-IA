FROM tensorflow/tensorflow:latest-gpu

#Update and Upgrade of OS
RUN apt-get update
RUN apt-get upgrade -y

#Update pip
RUN pip install --upgrade pip

COPY ./requirements.txt /tf/
COPY ./server/requirements.txt /tf/server/

#Install the requirements of the server
WORKDIR /tf/server
RUN pip install -r requirements.txt

CMD ["python", "server.py"]