#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

from PyGtalkRobot.PyGtalkRobot import GtalkRobot

from toodledoclient import *

############################################################################################################################

class RobotBean(GtalkRobot):
    def __init__(self, username, password, toodledo_appid):
        GtalkRobot.__init__(self)
        self.client = ToodledoClient(username, password, toodledo_appid)
    
    def command_001_setState(self, user, message, args):
        '''(available|online|on|busy|dnd|away|idle|out|off|xa)( +(.*))?$(?i)'''
        show = args[0]
        status = args[1]
        jid = user.getStripped()

        print "state"
        if jid == 'beanyoung.cn@gmail.com':
            print jid, " ---> ",self.getResources(jid), self.getShow(jid), self.getStatus(jid)
            self.setState(show, status)
            self.replyMessage(user, "State settings changed！")

    def command_002_nextBestAction(self, user, message, args):
        '''^[nN]\s*$'''
        print "next best action"
        ret_message = self.client.get_next_actions()
        self.replyMessage(user, ret_message)

    def command_003_listTask(self, user, message, args):
        #'''^[tT]\s+(?:f\.(\w+))?\s+(?:c\.(\w+))?\s+(?:p\.(\w+))?'''
        '''^[tT]\s+(.*)$'''
        ret_message = self.client.get_tasks(args[0])
        self.replyMessage(user, ret_message)

    def command_003_refresh(self, user, message, args):
        '''^(re|Re|RE|rE)$'''
        print 'reauthenticate'
        self.client.re_authenticate()
        ret_message = 're authenticated'
        self.replyMessage(user, ret_message)

