#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-


class Plan:
    def __init__(self, category="", duration=60):
        self.category = category
        self.duration = duration

    def setCategory(self, category):
        self.category = category

    def getCategory(self):
        return self.category

    def setDuration(self, duration):
        self.duration = duration

    def getDuration(self):
        return self.duration
