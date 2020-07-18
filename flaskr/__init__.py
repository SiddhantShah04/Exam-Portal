from flask import Flask
import os

# A application factory function,which create a Flask instance
def create_app(test_config=None):

    app = Flask(__name__,instance_relative_config=True)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.secret_key = "f*"
    
    from . import home
    app.register_blueprint(home.bp)

    from . import db
    db.init_app(app)

    from . import professor
    app.register_blueprint(professor.bp)

    from . import auth
    app.register_blueprint(auth.bp)
    
    @app.route("/hello")
    def hello():
        return("Hello World!")

    return app