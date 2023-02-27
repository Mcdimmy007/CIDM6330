import unittest
from datetime import datetime
from barkylib.domain.models import Bookmark
from barkylib.domain.commands import AddBookmarkCommand
from barkylib.adapters.repository import SqlAlchemyRepository
from barkylib.adapters.orm import metadata, start_mappers
from barkylib.services.adapters.orm import unit_of_work, SqlAlchemyUnitOfWork
from barkylib.services import BookmarkService
from barkylib import bootstrap

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, drop_database, database_exists

from ..flask_api import FlaskBookmarkAPI

class FlaskBookmarkAPITest(unittest.TestCase):
    def setUp(self):
        # Database Setup
        self.engine = create_engine('sqlite:///:memory:')
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        start_mappers()
        # Test bookmark created
        self.bookmark = Bookmark(
            id=None,
            title='Test Bookmark',
            url='http://www.testbookmark.com',
            notes='Test notes',
            date_added=datetime.utcnow(),
            category='test'
        )
        self.bookmark_service = BookmarkService(
            unit_of_work=SqlAlchemyUnitOfWork(session_factory=self.Session),
            repository=SqlAlchemyRepository(session_factory=self.Session)
        )
        self.bus = bootstrap.bootstrap()
        # Setting up Flask app and API
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = self.engine.url
        self.api = FlaskBookmarkAPI(bus=self.bus)
        app.add_url_rule('/', view_func=self.api.index)
        app.add_url_rule('/api/one/<id>', view_func=self.api.one)
        app.add_url_rule('/api/all', view_func=self.api.all)
        app.add_url_rule('/api/first/<filter>/<value>/<sort>', view_func=self.api.first)
        app.test_client_class= FlaskClient
        self.client = app.test_client()
    
    def tearDown(self):
        # Database Teardown
        drop_database(self.engine.url)
    
    def test_one(self):
        # Testing one method in the API
        response = self.client.get('/api/one/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), 'The provided id is 1')

    def test_all(self):
        # Testing the all method in the API
        response = self.client.get('/api/all')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), 'all records')
    
    def test_first(self):
        # Testing the first method of the API
        response = self.client.get('/api/first/category/test/date_added')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), 'the first ')
    
    def test_many(self):
        # Testing the many method of the API
        pass
    
    def test_add(self):
        # Testing the add method of the API
        command = AddBookmarkCommand(
            title=self.bookmark.title,
            url=self.bookmark.url,
            notes=self.bookmark.notes,
            date_added=self.bookmark.date_added,
            category=self.bookmark.category
        )
        response = self.client.post('/api/add', json=command.to_dict())
        self.assertEqual(response.status_code, 200)
        bookmark_dict = response.get_json()
        bookmark = Bookmark.from_dict(bookmark_dict)
        self
    