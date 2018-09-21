# JI-Live-Danmu-Server

## Usage:

1. Set server port and secret key in MessageQueue.py
```bash
vim MessageQueue.py
```
2. Run Live Danmu mq server
```bash
python MessageQueue.py
```
3. Set up qqbot
```bash
cp mqfeeder.py ~/.qqbot-tmp/plugins
qqbot -pl mqfeeder
```

## Run on docker

1. Build Dockerfile
```bash
docker build -t dmserver .
```
2. Run docker
```bash
docker run -it -p 6000:6000 -p 5001:5001 --name dmserver dmserver
```

QR code is on 0.0.0.0:5001

MQ is on 0.0.0.0:5000

Server will start with a random secretKey.
