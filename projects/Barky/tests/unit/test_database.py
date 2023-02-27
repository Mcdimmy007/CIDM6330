# pylint: disable=missing-module-docstring
from logging import Manager

from barkylib.services.database import DatabaseManager

from datetime import datetime


DatabaseManager.create_table('bookmarks', bookmarks_table)
cursor = db_manager._execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bookmarks'")
result = cursor.fetchone()

assert result[0] == 'bookmarks'

bookmark = {
    'title': 'WTAMU',
    'url': 'https://www.wtamu.edu/',
    'notes': 'School Website',
    'date_added': str(datetime.now())
}
DatabaseManager.add('bookmarks', bookmark)

# This is to delete the bookmark
DatabaseManager.delete('bookmarks', {'title': 'WTAMU'})

# Query to check if the bookmark was deleted
cursor = DatabaseManager.execute("SELECT * FROM bookmarks WHERE title='WTAMU")
result = cursor.fetchone()

assert result is None
