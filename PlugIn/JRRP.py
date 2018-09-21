import re
import numpy as np
import functools
import sys
import random

from .Utils import *

class JRRP:
    def __init__(self):
        self.coc_roll = r'(?:\!|\！)coc(:?7|)\s*\d*'

    async def process(self, bot, context):
        np.random.seed()
        msg = context['message']
        if bool(re.search(self.coc_roll, msg)):
            matches = re.findall(self.coc_roll_capture, msg)[0]
            version = 7 if matches[0] == '7' or matches[0] == '' else 6
            num_chars = int(matches[1])

            if num_chars > 10:
                await bot.send(context, '你投了好多好多次人物属性，kp都生气啦（惠惠小声地告诉你')
                return

            if version == 7:
                str = np.random.randint(1, 7, size=(3, num_chars)).sum(axis=0) * 5
                con = np.random.randint(1, 7, size=(3, num_chars)).sum(axis=0) * 5
                siz = (np.random.randint(1, 7, size=(2, num_chars)).sum(axis=0) + 6) * 5
                dex = np.random.randint(1, 7, size=(3, num_chars)).sum(axis=0) * 5
                app = np.random.randint(1, 7, size=(3, num_chars)).sum(axis=0) * 5
                inte = (np.random.randint(1, 7, size=(2, num_chars)).sum(axis=0) + 6) * 5
                pow = np.random.randint(1, 7, size=(3, num_chars)).sum(axis=0) * 5
                edu = (np.random.randint(1, 7, size=(2, num_chars)).sum(axis=0) + 6) * 5
                luck = np.random.randint(1, 7, size=(3, num_chars)).sum(axis=0) * 5

                total_ret = ''
                for i in range(num_chars):
                    total_ret += '力量: {} 体质: {} 体型: {} 敏捷: {} 外貌: {} 智力: {} 意志: {} 教育: {} 幸运: {} \n'.format(str[i],con[i],siz[i],dex[i],app[i],inte[i],pow[i],edu[i],luck[i])
            await bot.send(context, total_ret[:-1])
