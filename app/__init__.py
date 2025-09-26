from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.update(SECRET_KEY="dev", DATABASE="instance/app.db")

    @app.get("/")
    def index():
        return "OK", 200

    return app


# Usage:
# export FLASK_APP=app:create_app
# flask run --debug
