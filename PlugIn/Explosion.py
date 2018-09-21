import re
import numpy as np
import functools
import sys
import random

from .Utils import *

class Explosion:
    def __init__(self):
        self.scripts = ['比黑色更黑，比黑暗更暗的漆黑，在此寄讬吾真红的金光吧！觉醒之时的到来，荒谬教会的堕落章理，成为无形的扭曲而显现吧！起舞吧，起舞吧，起舞吧！吾之力量本源之愿的崩坏，无人可及的崩坏，将天地万象焚烧殆尽，自深渊降临吧，这就是人类最强威力的攻击手段，这就是究级攻击魔法， Explosion！', \
                        '我が名はめぐみん、红魔族随一の魔法の使い手にして、爆裂魔法を操りし者、我が力、见るが良い！Explosion!',\
                        '吾名惠惠，红魔族第一的魔法师兼爆裂魔法的操纵者，好好见识我的力量吧！Explosion!',\
                        '黒より黒く、 闇より暗き漆黒に、我が真红に混合を望みたろ、覚醒の时きたて、无谬の境界に落ちしことわり、无疆の歪み隣て 现世せよ！Explosion！',\
                        ]
    async def process(self, bot, context):
        np.random.seed()
