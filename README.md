# [Openpose-docker](https://hub.docker.com/repository/docker/talhailyas/openpose-v2/general)
Easy Install OpenPose Docker Image
* python>=3.6
* cuda:11.3.1
* cudnn8-devel
* ubuntu18.04
# Simple One Step installation (Updated)

If you use `v2` build you don't have to do any extra installation process.

```
docker pull talhailyas/openpose-v2:v0.1
```
Run in interactive model like; so you can use VS Code to attach the running container on remote or local server.

```
docker run --gpus all -it --rm -v /home/dir/to/mount/:/openpose/examples/media/ openpose-v2 /bin/bash
```
Check installation by;

```shell
root(inside_container)$ python3
>> import pyopenpose as op
>> 
```
or RUN with proper input, output dirs in background will exit once all videos processed in the input dir.

```
docker run --gpus "'device=0'" \
    -v /home/user01/Data/openpose/input:/openpose/input \
    -v /home/user01/Data/openpose/output:/openpose/output \
    -v /home/user01/Data/openpose/logs:/openpose/logs \
    -v /home/user01/Data/openpose/get_pose.py:/openpose/get_pose.py \
    talhailyas/openpose-v2:v0.1 /bin/bash -c "python3 /openpose/get_pose.py"
```

#### The `python` file `get_pose.py` is given in this github repo which you can download and load into docker image.
**Inside set `save_annotated_video=True` to save the pose annotated videos else set to `False` to only write `json` files.**


## Prerequistes

Requirements

*   Nvidia Docker runtime: https://github.com/NVIDIA/nvidia-docker#quickstart `nvidia-ctk`
*  CUDA 10.0 or higher on your host, check with `nvidia-smi`

## END
______________________________
# Version 1 (Only if you want to build with some sepecific settings.)
### Original `v2` Dockerfile used to build the `openpose-v2` image is below

`openpose-v1` file. Versions here only I labelled as my convenience don't have any impact on original source code at all.
```Dockerfile
FROM nvidia/cuda:11.3.1-cudnn8-devel-ubuntu18.04

#get deps
RUN apt-get update && \
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
python3-dev python3-pip python3-setuptools git g++ wget make libprotobuf-dev protobuf-compiler libopencv-dev \
libgoogle-glog-dev libboost-all-dev libcaffe-cuda-dev libhdf5-dev libatlas-base-dev

#for python api
RUN pip3 install --upgrade pip
RUN pip3 install numpy opencv-python 

#replace cmake as old version has CUDA variable bugs
RUN wget https://github.com/Kitware/CMake/releases/download/v3.16.0/cmake-3.16.0-Linux-x86_64.tar.gz && \
tar xzf cmake-3.16.0-Linux-x86_64.tar.gz -C /opt && \
rm cmake-3.16.0-Linux-x86_64.tar.gz
ENV PATH="/opt/cmake-3.16.0-Linux-x86_64/bin:${PATH}"

#get openpose
WORKDIR /openpose
RUN git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose.git .

#build it

COPY ./downloaded/models/ /openpose/models/

RUN mkdir -p /openpose/3rdparty/windows/caffe
RUN mkdir -p /openpose/3rdparty/windows/caffe3rdparty
RUN mkdir -p /openpose/3rdparty/windows/freeglut
RUN mkdir -p /openpose/3rdparty/windows/opencv
RUN mkdir -p /openpose/3rdparty/windows/spinnaker

COPY ./downloaded/3rdparty/caffe_16_2020_11_14.zip /openpose/3rdparty/windows/caffe/
COPY ./downloaded/3rdparty/caffe3rdparty_16_2020_11_14.zip /openpose/3rdparty/windows/caffe3rdparty/
COPY ./downloaded/3rdparty/freeglut_2018_01_14.zip /openpose/3rdparty/windows/freeglut/
COPY ./downloaded/3rdparty/opencv_450_v15_2020_11_18.zip /openpose/3rdparty/windows/opencv/
COPY ./downloaded/3rdparty/spinnaker_2018_01_24.zip /openpose/3rdparty/windows/spinnaker/

WORKDIR /openpose/build

RUN cmake -DBUILD_PYTHON=ON .. && make -j `nproc`
# Try with CUDA
# RUN cmake -D CUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda-11.3/bin/ -DBUILD_PYTHON=ON .. && make -j `nproc`
WORKDIR /openpose
``` 
You have to download the `models` and `3rdparty` models yourself. Use following links to do it. [#1602](https://github.com/CMU-Perceptual-Computing-Lab/openpose/issues/1602) and [#2230](https://github.com/CMU-Perceptual-Computing-Lab/openpose/issues/2230) or you can download from my Gdrive as below.

### Download these 2 links (G Driver):
G Drive version:

* Models: https://drive.google.com/file/d/1QCSxJZpnWvM00hx49CJ2zky7PWGzpcEh
* 3rdparty before 2021: https://drive.google.com/file/d/1mqPEnqCk5bLMZ3XnfvxA4Dao7pj0TErr
* 3rdparty for 2021 versions: https://drive.google.com/file/d/1WvftDLLEwAxeO2A-n12g5IFtfLbMY9mG

and then copy them in the  same dir as you Dockerfile.
### Build own your own
Copy the Dockerfile and the extracted zip model files in the same dir and then start build.
```
$ cd ./openpose-v0
$ sudo docker build -t openpose .
```
### Start container

```
$ docker run --gpus all -it --rm openpose
```

### Build Python Openpose

```
$ cd /openpose/build/python/openpose
$ make install
```

### When you start the container then you have to setup the env as following.

```
$ cd /openpose/build/python/openpose
$ cp ./pyopenpose.cpython-36m-x86_64-linux-gnu.so /usr/local/lib/python3.6/dist-packages
$ cd /usr/local/lib/python3.6/dist-packages
$ ln -s pyopenpose.cpython-36m-x86_64-linux-gnu.so pyopenpose
$ export LD_LIBRARY_PATH=/openpose/build/python/openpose
$ python3
>>> import pyopenpose as op
>>> 
```

# Version 2

Every time you have to set `env` when you restart the container if you don't wanna do this then you can setup these command as entry-point on container via shell script. 
Or simple use the v2 version.
```sh
docker pull talhailyas/openpose-v2
```
This one just has a defined entry-point the Dockerfile is below

```Dockerfile
FROM talhailyas/openpose-v1
COPY ./startup.sh /startup.sh
RUN chmod +x /startup.sh
ENTRYPOINT ["/startup.sh"]
```
and inside of shell file we have

```sh
$ cd /openpose/build/python/openpose
$ cp ./pyopenpose.cpython-36m-x86_64-linux-gnu.so /usr/local/lib/python3.6/dist-packages
$ cd /usr/local/lib/python3.6/dist-packages
$ ln -s pyopenpose.cpython-36m-x86_64-linux-gnu.so pyopenpose
$ export LD_LIBRARY_PATH=/openpose/build/python/openpose
$ cd /openpose
$ exec "$@"
```
#### References
* https://github.com/CMU-Perceptual-Computing-Lab/openpose
* https://hub.docker.com/r/cwaffles/openpose
