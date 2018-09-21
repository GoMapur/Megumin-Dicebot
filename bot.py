from aiocqhttp import CQHttp
import numpy as np

import sys, os

from PlugIn import *

bot = CQHttp(enable_http_post=False)
# TODO:
# 1. Explosion schedule
# 2. Parse Tree
# 3. Language suport
# 4. jrrp
# 5. Space in coc
# 6. COC and DND

other_bots_id = [1098894978, 3165402391]

dicer = Dicer()
repeater = Repeater()
recorder = Recorder('./Recorder_Data')
space_detecter = Space_Detecter()
coc_creater = COC_creater()

@bot.on_message()
async def handle_msg(context):
    await recorder.process(bot, context)

    if context['user_id'] not in other_bots_id:
        repeatable = True
        # .RD
        repeatable = not await dicer.process(bot, context) and repeatable
        # Detect space
        await space_detecter.process(bot, context)
        # COC7 Roller
        await coc_creater.process(bot, context)
        # Repeat
        if repeatable:
            await repeater.process(bot, context)




@bot.on_notice('group_increase')
async def handle_group_increase(context):
    await bot.send(context, message='欢迎新人～', is_raw=True)


@bot.on_request('group', 'friend')
async def handle_request(context):
    return {'approve': True}


bot.run(host='0.0.0.0', port=8080)
