#!/usr/bin/env python

from poodledo.poodledo import ApiClient

import types
import datetime

class ToodledoClient():
    def __init__(self, username, password, toodledo_appid):
        self.username = username
        self.password = password
        self.client = ApiClient(application_id = toodledo_appid)
        self.client.authenticate(username, password)

    def re_authenticate(self):
        self.client.authenticate(self.username, self.password)

    def get_tasks(self, message):
        task_condition = self._get_task_condition(message)
        folderID = 0
        if len(task_condition['f']) != 0:
            folder_list = self.client.getFolders()
            for folder in folder_list: 
                if folder.title == task_condition['f']:
                    folderID = folder.id

        contextID = 0 
        if len(task_condition['c']) != 0:
            context_list = self.client.getContexts()
            for context in context_list:
                if context.title == task_condition['c']:
                    contextID = context.id 

        if contextID != 0 and folderID != 0:
            tasks = self.client.getTasks(notcomp = 1,
                    folder = folderID,
                    context = contextID)
        elif contextID != 0 and folderID == 0:
            tasks = self.client.getTasks(notcomp = 1, context = contextID)
        elif contextID == 0 and folderID != 0:
            tasks = self.client.getTasks(notcomp = 1, folder = folderID)
        else:
            tasks = self.client.getTasks()
        ret_message = '' 
        print 'tasks types is :'
        print type(tasks)
        for k in sorted(tasks, key = lambda t:t.duedate):
            ret_message += "%s !%d %%%s\n" % (k.title, k.priority, k.duedate)
        return ret_message

    def _get_task_condition(self, cmd_string):
        task_condition = {'c':'', 'f':''} 
        task_condition_list = cmd_string.split(' ')
        for condition in task_condition_list:
            if len(condition) != 0:
                pos = condition.index('.')
                if pos == 1: 
                    task_condition[condition[0].lower()] = condition[2:]
        return task_condition 

    def get_next_actions(self):
        ret_message = ''
        today = datetime.datetime.today()
        after_day = today - datetime.timedelta(days = 1)
        before_day = today + datetime.timedelta(days = 2)
        after_time = after_day.strftime('%Y-%m-%d')
        before_time = before_day.strftime('%Y-%m-%d')
        tasks = self.client.getTasks(notcomp = 1,
                status = 1,
                after = after_time,
                before = before_time)
        print tasks
        # todo:sort tasks
        # for task in tasks:
        for task in sorted(tasks, key = lambda t:(t.duedate, -t.priority)):
            ret_message += "%s !%d %%%s\n" % (task.title,
                    task.priority,
                    task.duedate)

        return ret_message
