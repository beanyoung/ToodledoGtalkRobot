#!/usr/bin/env python

from beanrobot import *

bot = RobotBean('Toodledo Email', 'Toodledo Password', 'Toodledo AppID')
bot.setState('available', "Test Gtalk Robot")
bot.start("Gtalk Email", "Gtalk Password")
