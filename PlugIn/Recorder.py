import numpy as np
import pandas as pd
from datetime import datetime
from os.path import join, isfile

from .Utils import *

class Recorder:

    def __init__(self, dir_path):
        self.dir_path = dir_path
        exist_or_create(dir_path)
        self.accepted_message_type = ['private', 'group', 'discuss']
        for message_type in self.accepted_message_type:
            exist_or_create(join(dir_path, message_type))
        self.message_type2source = {'private':'user_id', 'group':'group_id', 'discuss':'discuss_id'}


    async def process(self, bot, context):
        if 'message_type' in context:
            message_type = context['message_type']
            source_key = self.message_type2source[message_type]
            source = context[source_key]

            df = pd.DataFrame(columns = context.keys())
            df = df.append(context, ignore_index=True)

            store_file = join(self.dir_path, message_type, str(source)+'.csv')
            if not isfile(store_file):
                df.to_csv(store_file, mode='w', header=True)
            else:
                df.to_csv(store_file, mode='a', header=False)
