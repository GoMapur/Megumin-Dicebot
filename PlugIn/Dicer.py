import re
import numpy as np
import functools
import sys

from .Utils import *

class Dicer:
    def __init__(self):
        self.math_expre_regex = r'(:?\(*(?:\+|\-)?\d+\)*(?:(?:\+|\-|\*|\/)\(*(?:\+|\-)?\d+\)*)+|\s*\(\s*\-?\s*\d+\s*\)\s*)'
        self.random_formula_regex = r'\s*\.\s*r\s*(?:\+|\-)?\s*\d*\s*d\s*(?:(?:\+|\-)?\s*\d+|(?:^\+|\-)?\s*\d*)\s*'
        self.random_formula_regex_capture = r'\s*\.\s*r\s*((?:\+|\-)?\s*\d*)\s*d\s*((?:(?:\+|\-)?\s*\d+|(?:^\+|\-)?\s*\d*))\s*'
        self.mathExpEval = MathExpEvaluator()

    async def process(self, bot, context):
        msg = context['message']
        if bool(re.search(self.random_formula_regex, msg)):
            try:
                formula = msg
                calculation_step = ''

                matches = re.findall(self.random_formula_regex, msg)
                while len(matches) != 0:
                    for match in matches:
                        nums = re.findall(self.random_formula_regex_capture, match)[0]
                        num_rolls = 1 if nums[0] == '' else int(remove_blank(nums[0]))
                        num_dice_sides = 100 if nums[1] == '' else int(remove_blank(nums[1]))
                        valid = await self.valid_param(bot, num_rolls, num_dice_sides)
                        if not valid:
                            return False
                        sign = 1 if num_rolls * num_dice_sides > 0 else -1
                        np.random.seed()
                        rand_nums = list(np.random.randint(1, np.abs(num_dice_sides)+1, size=np.abs(num_rolls)) * sign)
                        eval = np.sum(rand_nums)
                        if num_rolls != 1:
                            calculation_step += '(' + str(functools.reduce((lambda x, y: '{}, {}'.format(x,y)), rand_nums)) + ') = {}\n'.format(eval)
                        formula = re.sub(self.random_formula_regex, str(eval), formula, 1)

                    matches = re.findall(self.math_expre_regex, formula)
                    while len(matches) != 0:
                        for match in matches:
                            match = re.sub(r'\s', '', match)
                            eval = self.mathExpEval.eval_expr(match)
                            calculation_step +=  match + ' = {}\n'.format(eval)
                            formula = re.sub(self.math_expre_regex, str(eval), formula, 1)
                        matches = re.findall(self.math_expre_regex, formula)
                    matches = re.findall(self.random_formula_regex, formula)
                await bot.send(context, '{}\n{}'.format(formula, calculation_step)[:-1])
                return True
            except Exception as e:
                print(e, file=sys.stderr)
                await bot.send(context, '惠惠好像忘掉怎么算数了，嘿嘿（流口水')
        return False

    async def valid_param(self, bot, num_rolls, num_dice_sides):
        if num_rolls > 10000 and num_rolls != 0:
            await bot.send(context, "很快地，你的桌子被虚空中出现的成千上万名为骰子的怪物咂扁了。San Check，请。")
            return False
        if num_rolls == 0:
            await bot.send(context, "你扔了0个骰子。San Check，请。")
            return False
        if num_dice_sides > 10000 and num_dice_sides != 0:
            await bot.send(context, "你立刻意识到，这么多面的骰子就是一个球体，你和你的同伴因为朝上的究竟是哪一面开始争执起来。在发现你同伴其实是无形之子之后，你不得不做出退让，扔一面面数更少的骰子吧。")
            return False
        if num_dice_sides == 0:
            await bot.send(context, "你扔了个0面骰子。San Check，请。")
            return False
        return True
