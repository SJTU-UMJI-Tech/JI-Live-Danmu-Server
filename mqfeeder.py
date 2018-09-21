# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.parse import urlencode
from queue import Queue
import re
import threading as td
import sys
import time
import socket
TALK_FLAG = True
MY_SOCKET = None
MSG_Queue_Dict = {}


def waitForConnect():
    global MY_SOCKET
    while True:
        sock, addr = MY_SOCKET.accept()
        t = td.Thread(target=tcplink, args=(sock, addr))
        t.start()
        time.sleep(0.1)


def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    if (MSG_Queue_Dict.get(addr) is None):
        MSG_Queue_Dict[addr] = Queue()
        while True:
            if not MSG_Queue_Dict[addr].empty():
                try:
                    sock.send(
                        bytes(MSG_Queue_Dict[addr].get(), encoding="utf8"))
                except:
                    print("Unexpected error:", str(sys.exc_info()))
                    break
            else:
                time.sleep(0.1)
    MSG_Queue_Dict.pop()[addr]
    sock.shutdown(2)
    sock.close()


# def onPlug(bot):
    # global MY_SOCKET
print("init socket")
MY_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
MY_SOCKET.bind(('0.0.0.0', 6000))
MY_SOCKET.listen(5)
td.Thread(target=waitForConnect, daemon=True).start()


# qqbot onMessage event
def onQQMessage(bot, contact, member, content):
    global TALK_FLAG
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
