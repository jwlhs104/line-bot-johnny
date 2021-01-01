# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals
from stock_function import close_price, capacity, name, real_time, accu_capacity, accu_capacity_multi, estimated_capacity
from flex_template import flex_template, flex_template_multi
from photo import photo_dict
from queue import Queue

import os
import sys
from argparse import ArgumentParser
from time import time

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage, RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, URIAction
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)
stock_nums = {}
time_queue = Queue(maxsize = 3)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        # friend photo reponser
        if event.message.text in photo_dict:
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url=photo_dict[event.message.text],
                    preview_image_url=photo_dict[event.message.text]
                )
            )

        # rich menu linker
        if event.message.text == 'rich menu':
            user_id = event.source.user_id
            line_bot_api.link_rich_menu_to_user(user_id, rich_menu_id)

        # chat room id reponser
        if event.message.text == 'id':
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=str(event))
            )

        # stock information reponser
        if event.message.text[0] == 'V' or event.message.text[0] == 'v':

            # line_bot_api.reply_message(
            #     event.reply_token,
            #     TextSendMessage(text='欸你先等一下，證交所ban人啦')
            # )

            # return 'OK'

            stock_num = event.message.text[1:]
            stock_name = name(stock_num)
            stock_capacity = str(capacity(stock_num))
            stock_accu_capacity = str(accu_capacity(stock_num))
            stock_esti_capacity = str(estimated_capacity(stock_accu_capacity))

            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text = 'test',
                    contents = flex_template(stock_name, stock_capacity, stock_esti_capacity)
                )
            )

        # save stock number
        if event.message.text[0] == 'S' or event.message.text[0] == 's':
            print(list(time_queue.queue))
            if time_queue.full():
                if (time() - list(time_queue.queue)[0] < 6):
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text = '輸入過於頻繁, 請稍等再試')
                    )
                    return 'OK'
                else:
                    time_queue.get()
                    time_queue.put(time())
            else:
                time_queue.put(time())

            stock_num = event.message.text[1:]
            stock_nums.update({stock_num: capacity(stock_num)})
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='目前自選股票代號: ' + str([k for k,v in stock_nums.items()]))
            )


        # delete stock number

        if event.message.text[0] == 'D' or event.message.text[0] == 'd':
            stock_num = event.message.text[1:]
            stock_nums.pop(stock_num, None)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='目前自選股票代號: ' + str([k for k,v in stock_nums.items()]))
            )

        # delete all
        if event.message.text == '清空自選':
            stock_nums.clear()
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='目前自選股票代號: ' + str([k for k,v in stock_nums.items()]))
            )

        # print stock number
        if event.message.text == '預估量':
            print(list(time_queue.queue))
            if time_queue.full():
                if (time() - list(time_queue.queue)[0] < 5):
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text = '輸入過於頻繁, 請稍等再試')
                    )
                    return 'OK'
                else:
                    time_queue.get()
                    time_queue.put(time())
            else:
                time_queue.put(time())
            content = flex_template_multi(stock_nums)
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text = 'test',
                    contents = content
                )
            )


        # stock realtime information reponser
        if event.message.text[0] == 'R':

            stock_num = event.message.text[1:]
            stock_name = name(stock_num)
            stock_realtime = str(real_time(stock_num))

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=stock_realtime)
            )

        # test
        if event.message.text == 'test':
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=str('測試'))
            )
    return 'OK'



if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    # Run Response code
    app.run(debug=options.debug, port=options.port)

