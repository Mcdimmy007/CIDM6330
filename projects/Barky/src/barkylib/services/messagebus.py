# pylint: disable=unused-import
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from barkylib.adapters import orm, redis_eventpublisher
from barkylib.services import messagebus, unit_of_work

def app (environment="dev"):
    app = Flask(__name__)
    if environment == "dev":
        app.config["DEBUG"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dev.sqlite3"
    else:
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prod.sqlite3"


    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=False)
    session_factory = sessionmaker(bind=engine)
    orm.start_mappers()
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    pub = redis_eventpublisher.RedisEventPublisher()
    message_bus = messagebus.MessageBus(
        uow, event_handlers={}, command_handlers=messagebus.command_handlers(uow)
    
    )

    @app.route("/add_book", methods=["POST"])
    def add_book():
        data = request.get_json()
        command = commands.CreateBookCommand(
            data["title"], data["author"], data["published_date"], data["book_type"]
        )
        message_bus.handle(command)
        return jsonify({"message": "Book added successfully."})

    return app
