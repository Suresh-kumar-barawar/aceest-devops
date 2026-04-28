from flask import Flask

def create_app():
    app = Flask(__name__)

    from aceest.routes import register_routes
    register_routes(app)

    return app
