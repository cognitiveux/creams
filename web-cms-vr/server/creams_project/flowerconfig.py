import json
def format_task(task):
    #hide everything so that no sensitive information will be shown
    task.args = ''
    return task

#username & password for flower ui
import os
basic_auth = [os.environ['FLOWER_USER']+':'+os.environ['FLOWER_PASSWORD']]
