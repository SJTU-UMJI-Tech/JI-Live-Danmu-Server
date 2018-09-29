# JI-Live-Danmu-Server

## Usage:

1. Generate ssl cert
```bash
openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem
```
2. Set up qqbot
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

MQ is on 0.0.0.0:6000
