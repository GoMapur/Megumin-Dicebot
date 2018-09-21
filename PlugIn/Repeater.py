import numpy as np
import pandas as pd
from datetime import datetime

class Repeater:

    def __init__(self):
        self.last_messages = {}
        self.accepted_message_type = ['private', 'group', 'discuss']
        self.message_type2source = {'private':'user_id', 'group':'group_id', 'discuss':'discuss_id'}
        self.repeat_history = {}

    async def process(self, bot, context):
        original_context = context
        context = context.copy()
        if 'message_type' in context:
            message_type = context['message_type']
            source_key = self.message_type2source[message_type]
            source = context[source_key]

            current_time = context['time'] = np.datetime64(context['time'],'s')

            if source not in self.last_messages:
                self.last_messages[source] = pd.DataFrame(columns = context.keys())

            self.last_messages[source] = self.last_messages[source].append(context, ignore_index=True)

            self.last_messages[source] = self.last_messages[source][(self.last_messages[source]['time'] <= current_time) &
                                                    (self.last_messages[source]['time'] >= current_time - np.timedelta64(10, 'm'))]

            if source not in self.repeat_history:
                self.repeat_history[source] = pd.DataFrame(columns = ['time', 'message'])

            msg_rec = self.last_messages[source]

            counts_exlude_self = msg_rec[msg_rec['user_id'] != context['self_id']]
            counts_exlude_self = counts_exlude_self[counts_exlude_self['message'] == context['message']]['message'].value_counts()

            for msg, counts in counts_exlude_self.iteritems():
                if counts >= 2:
                    repeat_history = self.repeat_history[source][self.repeat_history[source]['message'] == msg]
                    if repeat_history.shape[0] != 0:
                        last_repeat = repeat_history.iloc[-1]
                        if last_repeat['time'] <= current_time - np.timedelta64(5, 'm'):
                            await self.repeat(bot, context, original_context)
                            return
                    else:
                        await self.repeat(bot, context, original_context)
                        return
            np.random.seed()
            if np.random.random_sample() > 0.99:
                await self.repeat(bot, context, original_context)
                return

    def record_repeat_history(self, context):
        message_type = context['message_type']
        source_key = self.message_type2source[message_type]
        source = context[source_key]

        rec_rep_history = self.repeat_history[source]
        if rec_rep_history[rec_rep_history['message'] == context['message']].shape[0] > 0:
            rec_rep_history.loc[rec_rep_history['message'] == context['message'], 'time'] = context['time']
            self.repeat_history[source] = rec_rep_history
        else:
            self.repeat_history[source] = self.repeat_history[source].append({'time': context['time'], 'message': context['message']}, ignore_index=True)

    async def repeat(self, bot, context, original_context):
        self.record_repeat_history(context)
        await bot.send(original_context, context['message'])
