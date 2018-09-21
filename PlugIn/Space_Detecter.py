from .Utils import *

class Space_Detecter:

    def __init__(self):
        self.accepted_message_type = ['private', 'group', 'discuss']
        self.message_type2source = {'private':'user_id', 'group':'group_id', 'discuss':'discuss_id'}


    async def process(self, bot, context):
        if 'message_type' in context:
            message_type = context['message_type']
            source_key = self.message_type2source[message_type]
            source = context[source_key]

            msg = context['message']
            if not msg[::2].strip() or (len(msg) > 1 and not msg[1:][::2].strip()):
                await bot.send(context, "这 人 说 话 带 空 格")
