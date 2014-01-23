#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

import pickle, os
from datetime import date, time, timedelta

class TodoList:
    """Todo list to appropriate day"""
    def __init__(self, _plans = {}):
        self.plans = {}
        self.addPlan(_plans)

    def getPlans(self):
        """Return all plans to this day"""
        return self.plans

    def addPlan(self, _plan):
        """Add plan  to this day. Also works as update"""
        for key, value in _plan.iteritems():
            if not value == None:
                self.plans[key] = value

    def removePlan(self, _plan):
        """Remove plan from this day"""
        if _plan in self.plans:
            del self.plans[_plan]
            return True
        else:
            return False


class TodoListContainer:
    """Container of todolists"""
    def __init__(self):
        self.todolists = {}
        self.todolistFile = ".todolist.tree"

    def fillTodolist(self):
        t = {date(2012,12,5) : {"A" : time(1), "B" : time(4)}}
        self.addTodolist(t)
        t = { date(2012,12,6) : {"A" : time(0,50), "B" : time(0,30)}}
        self.addTodolist(t)
        t = {date(2012,12,10) : {"B" : time(10)}}
        self.addTodolist(t)

    def addTodolist(self, _lst):
        """Add todolist to appropriate day. Also works as update"""
        for key, value in _lst.iteritems():
            if not value == None:
                self.todolists[key] = TodoList(value)
        self.storeTodolist()

    def getTodolists(self):
        return self.todolists

    def removeTodolist(self, _date):
        """Remove todolist from given day. It's like 'clear all day todolists'"""
        if _date in self.todolists:
            del self.todolists[_date]
        self.storeCategories()

    def findTodolist(self, _date):
        """Return todolist to requested day or None if not found"""
        if _date in self.todolists:
            return self.todolists[_date]
        return None

    def restoreTodolist(self):
        """Restore stored todolist"""
        if os.path.exists(self.todolistFile):
            f = open(self.todolistFile)
            self.todolists = pickle.load(f)
            f.close()

    def storeTodolist(self):
        """Store todolist into file to make them persistent"""
        f = open(self.todolistFile, "w+")
        pickle.dump(self.todolists, f)
        f.close()

    def clearTodolist(self):
        self.todolists = {}
