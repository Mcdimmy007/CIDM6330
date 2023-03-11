from flask import Flask, jsonify, request
from sqlalchemy.orm import Session

from barkylib.adapters.orm import SqlAlchemyBookmarkRepository
from barkylib.domain.models import Bookmark
from barkylib.services import handlers, messagebus, unit_of_work

# The new app is created
app = Flask(__name__)

# HTTP routes are defined
# The Routes call messagebus.handle() so as to pass commands to the right handler

@app.route("/bookmarks", methods=["GET"])
def list_bookmarks():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    with uow:
        bookmarks = handlers.list_bookmarks(
            request.args.get("order_by"), request.args.get("order"), uow
        )
    return jsonify([bookmark.to_dict() for bookmark in bookmarks])

@app.route("/bookmarks", methods=["POST"])
def add_bookmark():
    data = request.get_json()
    command = handlers.CreateBookmarkCommand(
        data["title"], data["url"], data.get("notes")
    )
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    with uow:
        messagebus.handle(command, uow)
        uow.commit()
    return ""

@app.route("/bookmarks/<bookmark_id>", methods=["PUT"])
def update_bookmark(bookmark_id):
    data = request.get_json()
    command = handlers.UpdateBookmarkCommand(
        bookmark_id, data.get("title"), data.get("url"), data.get("notes")
    )
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    with uow:
        messagebus.handle(command, uow)
        uow.commit()
    return ""

@app.route("/bookmarks/<bookmark_id>", methods=["DELETE"])
def delete_bookmark(bookmark_id):
    command = handlers.DeleteBookmarkCommand(bookmark_id)
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    with uow:
        messagebus.handle(command, uow)
        uow.commit()
    return ""

if __name__ == "__main__":
    app.run()