FROM tensorflow/tensorflow:latest-gpu

#Update and Upgrade of OS
RUN apt-get update
RUN apt-get upgrade -y

#Update pip
RUN pip install --upgrade pip

#Install latest version of tensorflow
RUN pip install tensorflow
RUN pip install jupyter

RUN pip install tf-models-official

WORKDIR /tf/
COPY ./requirements.txt /tf/
RUN pip install -r requirements.txt

RUN jupyter notebook --generate-config --allow-root
RUN echo "c.NotebookApp.password = u'sha1:6a3f528eec40:6e896b6e4828f525a6e20e5411cd1c8075d68619'" >> /root/.jupyter/jupyter_notebook_config.py
EXPOSE 8888
CMD ["jupyter", "notebook", "--allow-root", "--notebook-dir=/tf", "--ip=0.0.0.0", "--port=8888", "--no-browser"]