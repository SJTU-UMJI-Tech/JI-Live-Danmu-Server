# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.parse import urlencode
import re
TALK_FLAG = True


# qqbot onMessage event
def onQQMessage(bot, contact, member, content):
    # reply help content
    if re.search(r"#system ", content, re.I):
        if re.search(r"start", content):
            TALK_FLAG = True
        elif re.search(r"stop", content):
            TALK_FLAG = False
    # send message to queue
    if TALK_FLAG and not bot.isMe(contact, member):
            try:
                urlopen(
                    'http://127.0.0.1:5000/push?' + urlencode({
                        'message':
                        content
                    }),
                    timeout=1)
            except KeyError as e:
                print(e)
