# pylint: disable=syntax-error
import unittest
from datetime import datetime
from unittest.mock import patch
from barkylib.domain.commands import AddBookmarkCommand, DeleteBookmarkCommand, EditBookmarkCommand, ListBookmarksCommand
from barkylib.domain.models import Bookmark
from barkylib.services.handlers import add_bookmark, edit_bookmark, list_bookmarks 

class TestBookmarks(unittest.TestCase):
    
    def test_add_bookmark(self):
        command = AddBookmarkCommand(
            id=1,
            title="Test Bookmark",
            url="https://test.com",
            date_added=datetime.utcnow().isoformat(),
            date_edited=datetime.utcnow().isoformat(),
            notes="This is a test bookmark"
        )
        result = add_bookmark(command)
        self.assertTrue(result)
        
    def test_list_bookmarks(self):
        command = ListBookmarksCommand(order_by="id", order="asc")
        result = list_bookmarks(command)
        self.assertIsNotNone(result)
        
    def test_delete_bookmark(self):
        command = DeleteBookmarkCommand(id=1)
        result = DeleteBookmarkCommand(command)
        self.assertTrue(result)
        
    def test_edit_bookmark(self):
        command = EditBookmarkCommand(
            id=1,
            title="Edited Test Bookmark",
            url="https://editedtest.com",
            date_added=datetime.utcnow().isoformat(),
            date_edited=datetime.utcnow().isoformat(),
            notes="This is an edited test bookmark"
        )
        result = edit_bookmark(command)
        self.assertTrue(result)

