#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

from collections import Iterable
import json
import os


class Category(object):
    """Category contains activities"""

    def __init__(self, name="", activity=set()):
        self.name = name
        self.activities = set()
        self.add_activity(activity)

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


    def __str__(self):
        s = "Category: " + self.name + "\n"
        s += "Activities: " + str(self.activities) + "\n"
        return s

    def get_content(self):
        return {'name': self.name,
                'activities': list(self.activities)}


class CategoryContainer(object):
    """Container of categories"""

    def __init__(self, categoryFile):
        self.categories = set()
        self.categoryFile = categoryFile

    def __len__(self):
        return len(self.categories)

    def addCategory(self, category):
        if isinstance(category, Category):
            self.categories.add(category)
        elif isinstance(category, Iterable):
            self.categories.update(category)
        self.store()  # make the change persistent

    def deleteCategory(self, category):
        if isinstance(category, Category):
            self.categories.discard(category)
        elif isinstance(category, Iterable):
            self.categories.difference_update(category)
        elif isinstance(category, str):
            self.categories.discard(self.findCategory(category))
        self.store()  # make the change persistent

    def editCategory(self, oldCategory, newCategory):
        oldCategory.name = newCategory.name
        self.store()  # make the change persistent

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

    def restore(self):
        """Restore stored categories"""
        if os.path.exists(self.categoryFile):
            self.clearCategories()
            with open(self.categoryFile) as f:
                file_content = json.load(f)
            for category in file_content:
                self.addCategory(Category(category['name'],
                                          set(category['activities'])))

    def store(self):
        """Store categories into file to make them persistent"""
        with open(self.categoryFile, 'w+') as f:
            json.dump(self.get_content(), f, indent=1)

    def clearCategories(self):
        self.categories = set()

    def get_content(self):
        return [category.get_content() for category in self.categories]
