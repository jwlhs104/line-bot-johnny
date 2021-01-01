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

import os
import sys
from argparse import ArgumentParser

from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)


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


if __name__ == "__main__":

    import signal
    from apscheduler.schedulers.blocking import BlockingScheduler

    sched = BlockingScheduler(standalone=True)

    @sched.scheduled_job('cron', minute='51-55')
    def scheduled_job():
        line_bot_api.push_message(
                'Ce3ff54b6ef22f08a2e37c6e35a332634',
                TextSendMessage(text='機器人測試')
            )

    def gracefully_exit(signum, frame):
        print('Stopping...')
        sched.shutdown()

    signal.signal(signal.SIGINT, gracefully_exit)
    signal.signal(signal.SIGTERM, gracefully_exit)
    sched.start()

