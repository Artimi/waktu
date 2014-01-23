#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

class Plan:
    def __init__(self, _category = "", _duration = 60):
        self.category = _category
        self.duration = _duration

    def setCategory(self, _category):
        self.category = _category

    def getCategory(self):
        return self.category

    def setDuration(self, _duration):
        self.duration = _duration

    def getDuration(self):
        return self.duration
