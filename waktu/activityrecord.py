#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

from activity import Activity
from time import time


class ActivityRecord:
    """Contains record about every activity"""
    def __init__(self, category='', activity=Activity(), startTime=time(), endTime=time()):
        self.category = category
        self.activity = activity
        self.startTime = startTime
        self.endTime = endTime
