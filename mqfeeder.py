# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.parse import urlencode
from queue import Queue
import re
import threading as td
import sys
import time
import socket
import ssl
import os
TALK_FLAG = True
MY_SOCKET = None
MSG_Queue_Dict = {}


def waitForConnect():
    global MY_SOCKET
    while True:
        try:
            sock, addr = MY_SOCKET.accept()
            connStream = ssl.wrap_socket(
                sock,
                "key.pem",
                "cert.pem",
                server_side=True,
                ssl_version=ssl.PROTOCOL_TLSv1)
            t = td.Thread(target=tcplink, args=(connStream, addr))
            t.start()
        except:
            print("Unexpected error:", str(sys.exc_info()))
        time.sleep(0.1)


def tcplink(connStream, addr):
    global MSG_Queue_Dict
    print('Accept new connection from %s:%s...' % addr)
    if (MSG_Queue_Dict.get(addr) is None):
        MSG_Queue_Dict[addr] = Queue()
        while True:
            if not MSG_Queue_Dict[addr].empty():
                try:
                    myByte = bytes(
                        MSG_Queue_Dict[addr].get().replace('\0', '') + '\0',
                        encoding="utf8")
                    connStream.send(myByte)
                except:
                    print("Unexpected error:", str(sys.exc_info()))
                    break
            else:
                time.sleep(0.1)
    MSG_Queue_Dict.pop()[addr]
    connStream.shutdown(socket.SHUT_RDWR)
    connStream.close()


<<<<<<< HEAD
def onPlug(bot):
    global MY_SOCKET
    print("init socket")
    print(os.path.abspath('.'))
    print('path end')
    MY_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    MY_SOCKET.bind(('0.0.0.0', 6000))
    MY_SOCKET.listen(5)
    td.Thread(target=waitForConnect, daemon=True).start()
=======
# def onPlug(bot):
    # global MY_SOCKET
print("init socket")
MY_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
MY_SOCKET.bind(('0.0.0.0', 6000))
MY_SOCKET.listen(5)
td.Thread(target=waitForConnect, daemon=True).start()
>>>>>>> 6d106d3062984a07f41f3c8deeee52854716e1b7


# qqbot onMessage event
def onQQMessage(bot, contact, member, content):
    global TALK_FLAG, MSG_Queue_Dict
    if re.search(r"#system ", content, re.I):
        if re.search(r"start", content):
            TALK_FLAG = True
        elif re.search(r"stop", content):
            TALK_FLAG = False
    # send message to queue
    if TALK_FLAG and not bot.isMe(contact, member):
        try:
            for queue in MSG_Queue_Dict.values():
                queue.put(content)
        except KeyError as e:
            print(e)
