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

    def setActivity(self, activity):
        self.activity = activity

    def getActivity(self):
        return self.activity

    def setCategory(self, category):
        self.category = category

    def getCategory(self):
        return self.category

    def setStartTime(self, startTime):
        self.startTime = startTime

    def getStartTime(self):
        return self.startTime

    def setEndTime(self, endTime):
        self.endTime = endTime

    def getEndTime(self):
        return self.endTime
