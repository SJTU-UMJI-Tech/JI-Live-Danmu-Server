from flask import Flask, request
from queue import Queue
import argparse
import sys
import random
import string

SECRET_KEY = 'YourSecretKey'

app = Flask(__name__)

q = Queue()

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
userIP = '127.0.0.1'

# identify user's identity
@app.route("/")
def hello():
    global userIP
    if request.args.get('secretKey') == SECRET_KEY:
        userIP = request.remote_addr
    return "Hello World!"

# add message to queue
@app.route("/push")
def push():
    if request.remote_addr != '127.0.0.1':
        return 'Error:403 Forbidden'
    message = request.args.get('message')
    q.put(message)
    return 'OK'

# get message to queue
@app.route("/get")
def get():
    if request.remote_addr not in [userIP, '127.0.0.1']:
        return 'Error:403 Forbidden'
    if q.empty():
        return 'Error:Empty'
    else:
        return q.get()

# remove all messages in queue
@app.route("/cls")
def cls():
    if request.remote_addr not in [userIP, '127.0.0.1']:
        return 'Error:403 Forbidden'
    with q.mutex:
        q.queue.clear()
    return 'OK'

# get queue length
@app.route("/qsize")
def qsize():
    if request.remote_addr not in [userIP, '127.0.0.1']:
        return 'Error:403 Forbidden'
    return str(q.qsize())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='JI Live Danmu Server.')
    parser.add_argument('-ip', default='0.0.0.0', type=str)
    parser.add_argument('-port', default='5000', type=str)
    parser.add_argument('-sk', default='YourSecretKey', type=str)
    args = vars(parser.parse_args())
    SECRET_KEY = args['sk']
    if SECRET_KEY == 'YourSecretKey':
        SECRET_KEY = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    print('Your Secret Key: '+SECRET_KEY)
    app.run(host=args['ip'], port=args['port'])
