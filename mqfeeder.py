# -*- coding: utf-8 -*-
from qqbot.utf8logger import INFO, ERROR
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote
from queue import Queue
import re
import threading as td
import sys
import time
import socket
import ssl
import os
import json
import random
TALK_FLAG = True
MY_SOCKET = None
MSG_Queue_Dict = {}
GIFT_COUNTDOWN = -1


def waitForConnect():
    global MY_SOCKET
    while True:
        try:
            sock, addr = MY_SOCKET.accept()
            if (MSG_Queue_Dict.get(addr) is None):
                connStream = ssl.wrap_socket(
                    sock,
                    "key.pem",
                    "cert.pem",
                    server_side=True,
                    ssl_version=ssl.PROTOCOL_TLSv1)
                t = td.Thread(target=tcplink, args=(connStream, addr))
                t.start()
            else:
                pass
        except:
            ERROR("Unexpected error in waitForConnect:" + str(sys.exc_info()))
        time.sleep(0.1)


def tcplink(connStream, addr):
    global MSG_Queue_Dict
    INFO('Accept new connection from %s:%s...' % addr)
    MSG_Queue_Dict[addr] = Queue()
    while True:
        if not MSG_Queue_Dict[addr].empty():
            try:
                myByte = bytes(
                    MSG_Queue_Dict[addr].get().replace('\0', '') + '\0',
                    encoding="utf8")
                connStream.send(myByte)
            except ConnectionResetError:
                INFO("Connection reset...")
                break
            except:
                ERROR("Unexpected error:" + str(sys.exc_info()))
                break
        else:
            time.sleep(0.1)
    MSG_Queue_Dict.pop(addr)
    connStream.shutdown(socket.SHUT_RDWR)
    connStream.close()
    INFO('Close connection with %s:%s...' % addr)


def verify(word):
    ret = ''
    api_url = 'https://aip.baidubce.com/rest/2.0/antispam/v2/spam'
    paramas = {'access_token': '', 'content': word}
    paramas = urlencode(paramas).encode('utf-8')
    labels_type = {
        1: '暴恐违禁',
        2: '文本色情',
        3: '政治敏感',
        4: '恶意推广',
        5: '低俗辱骂',
        6: '低质灌水',
    }
    try:
        response = Request(api_url, data=paramas)
        response = urlopen(response).read()
        for error in json.loads(response)['result']['reject']:
            for hit in error['hit']:
                ret = ret + hit + ' '
            ret = ret + ' 涉嫌' + labels_type[error['label']] + '\n'
        for error in json.loads(response)['result']['review']:
            for hit in error['hit']:
                ret = ret + hit
            ret = ret + ' 涉嫌' + labels_type[error['label']] + '\n'
        return ret
    except:
        print('verify error')
        return ''


def onPlug(bot):
    global MY_SOCKET
    INFO("init socket")
    MY_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    MY_SOCKET.bind(('0.0.0.0', 6000))
    MY_SOCKET.listen(5)
    td.Thread(target=waitForConnect, daemon=True).start()


# qqbot onMessage event
def onQQMessage(bot, contact, member, content):
    global GIFT_COUNTDOWN
    try:
        global TALK_FLAG, MSG_Queue_Dict
        if re.search(r'\[.+\]请使用.+进行查看', content):
            return
        content = re.sub(r'\[@ME\]', '', content)
        if re.search(r"#system ", content, re.I):
            if re.search(r"danmu on", content):
                TALK_FLAG = True
            elif re.search(r"danmu off", content):
                TALK_FLAG = False
            elif re.search(r"gift start", content):
                INFO("Gift mode start")
                GIFT_COUNTDOWN = random.randint(11, 20)
        # send message to queue
        if TALK_FLAG and content and not bot.isMe(
                contact, member) and contact.ctype == "group":
            verify_result = verify(content)
            if verify_result:
                bot.SendTo(contact, verify_result[:-1])
            else:
                if GIFT_COUNTDOWN == 1:
                    GIFT_COUNTDOWN = -1
                    bot.SendTo(
                        contact, "Congratulations!\r\n" + "[" + member.name +
                        "]:[" + content + "]" + "get the gift!")
                elif GIFT_COUNTDOWN > 1:
                    INFO('Gift Countdown:' + str(GIFT_COUNTDOWN))
                    GIFT_COUNTDOWN -= 1
                for queue in MSG_Queue_Dict.values():
                    queue.put(content)
    except:
        ERROR("Unexpected error in onQQMessage:" + str(sys.exc_info()))
