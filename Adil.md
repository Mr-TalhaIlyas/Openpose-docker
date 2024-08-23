
Hi Adil,

Hope you are well.

Can you kindly run the following docker file to generate the pose of the video files we recently ran the other docker imager.

1. Pull Docker from source, this might take a few minutes to download the image.
```
 docker pull talhailyas/openpose-v2:v0.1
```
2. Then just like the last docker file we ran you can ran the following command, just change the path to where the input videos are,
```
docker run --gpus all 
    -v /home/user01/Data/input:/openpose/input 
    -v /home/user01/Data/output:/openpose/output 
    -v /home/user01/Data/logs:/openpose/logs 
    -v /home/user01/Data/get_pose.py:/openpose/get_pose.py 
    talhailyas/openpose-v2:v0.1 /bin/bash -c "python3 /openpose/get_pose.py"
```
There is one difference: you have to upload  the get_pose.py script on the Alfred server and also add its path in the docker run command as shown in the second last line.

The python script is attached to this email.

Kindly let me know when you run it or if you face any issues with it.

NOTE: Remember last time we had to remove the spaces between the new lines  to make it work, here I just wrote in separate lines so you can easily update the paths.

Best Regards,
Talha ILyas
