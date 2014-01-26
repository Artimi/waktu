#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

from collections import Iterable
import pickle
import os


class Category(object):
    """Category contains activities and tarification"""

    def __init__(self, name="", activity=set(), tarif=()):
        self.name = name
        self.activities = set()
        self.add_activity(activity)
        self.tarif = tarif

    def add_activity(self, activity):
        if isinstance(activity, str):
            self.activities.add(activity)
        elif isinstance(activity, Iterable):
            self.activities.update(activity)

    def delete_activity(self, activity):
        if isinstance(activity, str):
            self.activities.discard(activity)
        elif isinstance(activity, Iterable):
            self.activities.difference_update(activity)

    def containsActivity(self, activity):
        if activity in self.activities:
            return True
        else:
            return False

    @property
    def tarif(self):
        try:
            if len(self.tarif) == 0:
                return None
            else:
                return self.tarif
        except:
            return None

    @tarif.setter
    def tarif(self, tarif):
        try:
            if len(tarif) == 2:
                self.tarif = tarif
        except:
            pass

    def __str__(self):
        s = "Category: " + self.name + "\n"
        s += "Activities: " + str(self.activities) + "\n"
        s += "Tarif: " + str(self.tarif)
        return s


class CategoryContainer:
    """Container of categories"""
    def __init__(self, categoryFile):
        self.categories = set()
        self.categoryFile = categoryFile

    def addCategory(self, category):
        if isinstance(category, Category):
            self.categories.add(category)
        elif isinstance(category, Iterable):
            self.categories.update(category)
        self.storeCategories()  # make the change persistent

    def deleteCategory(self, category):
        if isinstance(category, Category):
            self.categories.discard(category)
        elif isinstance(category, Iterable):
            self.categories.difference_update(category)
        elif isinstance(category, str):
            self.categories.discard(self.findCategory(category))
        self.storeCategories()  # make the change persistent

    def editCategory(self, oldCategory, newCategory):
        oldCategory.name = newCategory.name
        oldCategory.tarif = newCategory.tarif
        self.storeCategories()  # make the change persistent

    def findCategory(self, categoryName):
        for cat in self.categories:
            if cat.name == categoryName:
                return cat
        return None

    def getContainingCategories(self, activity):
        """Return a list of categories where the given activity
        is included"""
        result = []
        for category in self.categories:
            if category.containsActivity(activity.name):
                result.append(category)
        return result

    def restoreCategories(self):
        """Restore stored categories"""
        if os.path.exists(self.categoryFile):
            with open(self.categoryFile) as f:
                self.categories = pickle.load(f)

    def storeCategories(self):
        """Store categories into file to make them persistent"""
        with open(self.categoryFile, "w+") as f:
            pickle.dump(self.categories, f)

    def clearCategories(self):
        self.categories = set()
