#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

from collections import Iterable
import pickle, os

class Category(object):
    """Category contains activities and tarification"""

    def __init__(self, name="", _activity=set(), tarif=()):
        self._name = name
        self._activities = set()
        self.add_activity(_activity)
        self._tarif = tarif

    @property
    def activities(self):
        return self._activities

    def add_activity(self, _activity):
        if isinstance(_activity, str):
            self._activities.add(_activity)
        elif isinstance(_activity, Iterable):
            self._activities.update(_activity)

    def delete_activity(self, _activity):
        if isinstance(_activity, str):
            self._activities.discard(_activity)
        elif isinstance(_activity, Iterable):
            self._activities.difference_update(_activity)

    def containsActivity(self, _activity):
        if _activity in self._activities:
            return True
        else:
            return False

    @property
    def tarif(self):
		try:
			if len(self._tarif) == 0:
				return None
			else:
				return self._tarif
		except:
			return None

    @tarif.setter
    def tarif(self, tarif):
        try:
            if len(tarif) == 2:
                self._tarif = tarif
        except:
            pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def __str__(self):
        s = "Category: " + self._name + "\n"
        s += "Activities: " + str(self._activities) + "\n"
        s += "Tarif: " + str(self._tarif)
        return s


class CategoryContainer:
    """Container of categories"""
    def __init__(self):
        self.categories = set()
        self.categoryFile = ".categories.tree"

    def fillCategory(self):
        c = Category("Projekt ABC",["Firefox", "CodeBlocks", "gedit", "Terminal"],(120,"CZK"))
        self.addCategory(c)
        c = Category("Projekt XYZ",["Firefox", "Terminal"],(100,"CZK"))
        self.addCategory(c)
        c = Category("Zabava",[])
        self.addCategory(c)

    def getCategories(self):
        return self.categories


    def addCategory(self, _cat):
        if isinstance(_cat, Category):
            self.categories.add(_cat)
        elif isinstance(_cat, Iterable):
            self.categories.update(_cat)
        self.storeCategories() # make the change persistent

    def deleteCategory(self, _cat):
        if isinstance(_cat, Category):
            self.categories.discard(_cat)
        elif isinstance(_cat, Iterable):
            self.categories.difference_update(_cat)
        elif isinstance(_cat, str):
            self.categories.discard(self.findCategory(_cat))
        self.storeCategories() # make the change persistent

    def editCategory(self, _oldCat, _newCat):
        _oldCat.name = _newCat.name
        _oldCat.tarif = _newCat.tarif
        self.storeCategories() # make the change persistent

    def findCategory(self, _catName):
        for cat in self.categories:
            if cat.name == _catName:
                return cat
        return None

    def getContainingCategories(self, _activity):
        """Return a list of categories where the given activity
        is included"""
        _result = []
        for cat in self.categories:
            if cat.containsActivity(_activity.getName()):
                _result.append(cat)
        return _result

    def restoreCategories(self):
        """Restore stored categories"""
        if os.path.exists(self.categoryFile):
            f = open(self.categoryFile)
            self.categories = pickle.load(f)
            f.close()

    def storeCategories(self):
        """Store categories into file to make them persistent"""
        f = open(self.categoryFile, "w+")
        pickle.dump(self.categories,f)
        f.close()

    def clearCategories(self):
        self.categories = set()
