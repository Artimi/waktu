#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

import pickle
import os


class TodoList(object):
    """Todo list to appropriate day"""
    def __init__(self, plans={}):
        self.plans = {}
        self.addPlan(plans)

    def getPlans(self):
        """Return all plans to this day"""
        return self.plans

    def addPlan(self, plan):
        """Add plan  to this day. Also works as update"""
        for key, value in plan.iteritems():
            if not value is None:
                self.plans[key] = value

    def removePlan(self, plan):
        """Remove plan from this day"""
        if plan in self.plans:
            del self.plans[plan]
            return True
        else:
            return False


class TodoListContainer(object):
    """Container of todolists"""
    def __init__(self, todolistFile):
        self.todolists = {}
        self.todolistFile = todolistFile

    def addTodolist(self, lst):
        """Add todolist to appropriate day. Also works as update"""
        for key, value in lst.iteritems():
            if not value is None:
                self.todolists[key] = TodoList(value)
        self.storeTodolist()

    def getTodolists(self):
        return self.todolists

    def removeTodolist(self, dat):
        """Remove todolist from given day. It's like 'clear all day todolists'"""
        if dat in self.todolists:
            del self.todolists[dat]
        self.storeCategories()

    def findTodolist(self, dat):
        """Return todolist to requested day or None if not found"""
        if dat in self.todolists:
            return self.todolists[dat]
        return None

    def restoreTodolist(self):
        """Restore stored todolist"""
        if os.path.exists(self.todolistFile):
            with open(self.todolistFile) as f:
                self.todolists = pickle.load(f)

    def storeTodolist(self):
        """Store todolist into file to make them persistent"""
        with open(self.todolistFile, "w+") as f:
            pickle.dump(self.todolists, f)

    def clearTodolist(self):
        self.todolists = {}
