# JI-Live-Danmu-Server

Usage:
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
