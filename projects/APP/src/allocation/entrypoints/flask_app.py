# pylint: disable=broad-except
from datetime import date
from flask import Flask, request, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker
from allocation.domain import model
from allocation.service_layer import unit_of_work, handlers, messagebus

def create_app(engine, test_config=None):
    app = Flask(__name__)
    session_maker = scoped_session(sessionmaker(bind=engine))

    @app.route("/schoolwork")
    def schoolwork():
        return "OK", 200

    @app.route("/allocate", methods=["POST"])
    def allocate():
        try:
            data = request.get_json()
            assert data is not None
            line_to_allocate = model.OrderLine(
                data["order_reference"],
                data["sku"],
                data["quantity"],
            )
            batch_ref = handlers.allocate(
                line_to_allocate, unit_of_work.SQLAlchemyUnitOfWork(session_maker)
            )
            return jsonify({"batch_ref": batch_ref}), 201
        except (KeyError, AssertionError):
            return jsonify({"error": "Invalid JSON data"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/add_batch", methods=["POST"])
    def add_batch():
        try:
            data = request.get_json()
            assert data is not None
            eta = data.get("eta")
            if eta is None:
                eta = date.today()
            batch_ref = handlers.add_batch(
                unit_of_work.SQLAlchemyUnitOfWork(session_maker),
                data["reference"],
                data["sku"],
                data["available_quantity"],
                eta,
            )
            return jsonify({"batch_ref": batch_ref}), 201
        except (KeyError, AssertionError):
            return jsonify({"error": "Invalid JSON data"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app
