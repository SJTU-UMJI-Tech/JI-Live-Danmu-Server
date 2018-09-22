# base image
FROM python:3.6

# change dir to /root
WORKDIR /root

# running required command
RUN pip install qqbot

# put files
ADD mqfeeder.py /root/.qqbot-tmp/plugins/mqfeeder.py
ADD cert.pem /root/cert.pem
ADD key.pem /root/key.pem

EXPOSE 6000
EXPOSE 5001

# Start the server
CMD qqbot -pl mqfeeder -ip 0.0.0.0 -hp 5001
