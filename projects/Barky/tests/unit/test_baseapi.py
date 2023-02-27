import unittest
from abc import ABC, abstractmethod

from barkylib.api.baseapi import AbstractBookMarkAPI

class AbstractBookMarkAPITest(unittest.TestCase):
    class TestAPI(AbstractBookMarkAPI):
        def one(self, id):
           return {'id': id}

        def first(self, property, value):
            return {'property': property, 'value': value}

        def many(self, property, value, sort):
            return {'property': property, 'value': value, 'sort': sort}

        def add(self, bookmark):
            return bookmark

        def delete(self, bookmark):
            return True

        def update(self, bookmark):
            return bookmark

    def test_one(self):
        api = self.TestAPI()
        result = api.one(1)
        self.assertEqual(result, {'id': 1})

    def test_first(self):
        api = self.TestAPI()
        result = api.first('class', 'System Development')
        self.assertEqual(result, {'property': 'class', 'value': 'System Development'})

    def test_many(self):
        api = self.TestAPI()
        result = api.many('group', 'system design', 'date_added')
        self.assertEqual(result, {'property': 'group', 'value': 'system design', 'sort': 'date_added'})

    def test_add(self):
        api = self.TestAPI()
        bookmark = {'title': 'System Development Class', 'url': 'https://www.wtamu.edu', 'category': 'system design'}
        result = api.add(bookmark)
        self.assertEqual(result, bookmark)

    def test_delete(self):
        api = self.TestAPI()
        bookmark = {'id': 1, 'title': 'System Development Class', 'url': 'https://www.wtamu.edu', 'category': 'system design'}
        result = api.delete(bookmark)
        self.assertEqual(result, True)

    def test_update(self):
        api = self.TestAPI()
        bookmark = {'id': 1, 'title': 'System Development Class', 'url': 'https://www.wtamu.edu', 'category': 'system design'}
        result = api.update(bookmark)
        self.assertEqual(result, bookmark)

if __name__ == '__main__':
    unittest.main()
