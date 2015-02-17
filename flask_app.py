from flask import Flask
from sqlalchemy import create_engine

from myapp import config
from myapp.views import frontend

def create_app(database_uri, debug=False):
    app = Flask(__name__)
    app.debug = debug

    # set up your database
    app.engine = create_engine(database_uri)

    # add your modules
    app.register_module(frontend)
    
    # other setup tasks

    return app
if __name__ == "__main__":
    app = create_app(config.DATABASE_URI, debug=True)
    app.run()
