# base image
FROM python:3.6

# MAINTAINER
MAINTAINER 1328410180@qq.com

# change dir to /root
WORKDIR /root

# running required command
RUN pip install qqbot flask pillow wcwidth

# put files
ADD MessageQueue.py /root/MessageQueue.py
ADD mqfeeder.py /root/.qqbot-tmp/plugins/mqfeeder.py

EXPOSE 5000
EXPOSE 5001

# Start the server
CMD qqbot -pl mqfeeder -ip 0.0.0.0 -hp 5001 -dm; python MessageQueue.py
