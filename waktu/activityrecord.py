#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

import category
from activity import Activity
from category import Category
from time import time

class ActivityRecord:
	"""Contains record about every activity"""
	def __init__(self, _category='', _activity=Activity(), _startTime=time(), _endTime=time()):
		self.category = _category
		self.activity = _activity
		self.startTime = _startTime
		self.endTime = _endTime
		
	def setActivity(self, _activity):
		self.activity = _activity
		
	def getActivity(self):
		return self.activity
		
	def setCategory(self, _category):
		self.category = _category
		
	def getCategory(self):
		return self.category
		
	def setStartTime(self, _startTime):
		self.startTime = _startTime
		
	def getStartTime(self):
		return self.startTime
		
	def setEndTime(self, _endTime):
		self.endTime = _endTime
	
	def getEndTime(self):
		return self.endTime
