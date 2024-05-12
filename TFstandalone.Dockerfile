FROM tensorflow/tensorflow:latest-gpu

#Update and Upgrade of OS
RUN apt-get update
RUN apt-get upgrade -y

#Update pip
RUN pip install --upgrade pip

#Install latest version of tensorflow
RUN pip install tensorflow
RUN pip install jupyter

#Installing python packages
#RUN pip install pillow lxml

#Installing system packages
#RUN apt-get install -y protobuf-compiler git

#WORKDIR /tf/tensorflow/

#Download tensorflow models
#RUN git clone https://github.com/tensorflow/models.git
#WORKDIR /tf/tensorflow/models/research

#RUN ls

#Run protoc
#RUN protoc object_detection/protos/*.proto --python_out=.
#RUN export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim


#WORKDIR /tf/tensorflow/models/research
#RUN cp object_detection/packages/tf2/setup.py .
#RUN pip install .

#RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

#RUN pip install protobuf==3.20.*
#RUN pip install tensorflow==2.15.*
#RUN pip install wget
#RUN pip install lvis
RUN pip install tf-models-official

RUN jupyter notebook --generate-config --allow-root
RUN echo "c.NotebookApp.password = u'sha1:6a3f528eec40:6e896b6e4828f525a6e20e5411cd1c8075d68619'" >> /root/.jupyter/jupyter_notebook_config.py
EXPOSE 8888
CMD ["jupyter", "notebook", "--allow-root", "--notebook-dir=/tf", "--ip=0.0.0.0", "--port=8888", "--no-browser"]