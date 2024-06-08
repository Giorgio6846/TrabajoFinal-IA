FROM tensorflow/tensorflow:latest-gpu

#Update and Upgrade of OS
RUN apt-get update
RUN apt-get upgrade -y

#Update pip
RUN pip install --upgrade pip

#Install latest version of tensorflow
RUN pip install tensorflow