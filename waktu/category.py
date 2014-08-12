#-*- coding: UTF-8 -*-
"""
Waktu module for category related object. A Category in context of
Waktu is a class containing activities which can represent e.g. Work,
School or any other meaningfull area.
"""
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

    def __contains__(self, activity):
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

    def __init__(self, category_file):
        self.categories = set()
        self.category_file = category_file

    def __len__(self):
        return len(self.categories)

    def add(self, category):
        if isinstance(category, Category):
            self.categories.add(category)
        elif isinstance(category, Iterable):
            self.categories.update(category)
        self.store()  # make the change persistent

    def delete(self, category):
        if isinstance(category, Category):
            self.categories.discard(category)
        elif isinstance(category, Iterable):
            self.categories.difference_update(category)
        elif isinstance(category, str):
            self.categories.discard(self.find(category))
        self.store()  # make the change persistent

    def edit(self, old_category, new_category):
        old_category.name = new_category.name
        self.store()  # make the change persistent

    def find(self, category_name):
        for cat in self.categories:
            if cat.name == category_name:
                return cat
        return None

    def get_containing_categories(self, activity):
        """Return a list of categories where the given activity
        is included"""
        result = []
        for category in self.categories:
            if activity.name in category:
                result.append(category)
        return result

    def restore(self):
        """Restore stored categories"""
        if os.path.exists(self.category_file):
            self.clear()
            with open(self.category_file) as f:
                file_content = json.load(f)
            for category in file_content:
                self.add(Category(category['name'], set(category['activities'])))

    def store(self):
        """Store categories into file to make them persistent"""
        with open(self.category_file, 'w+') as f:
            json.dump(self.get_content(), f, indent=1)

    def clear(self):
        self.categories = set()

    def get_content(self):
        return [category.get_content() for category in self.categories]
