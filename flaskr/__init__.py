import os

from flask import Flask, send_from_directory

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "parts.sqlite"),
        DATA_DIR=os.path.join(app.root_path, 'data'),
        UPLOAD_DIR=os.path.join(app.instance_path,'uploads')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the various directories exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    try:
        os.makedirs(app.config['DATA_DIR'])
    except OSError:
        pass

    try:
        os.makedirs(app.config['UPLOAD_DIR'])
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    from flaskr import db

    db.init_app(app)

    # apply the blueprints to the app
    from flaskr import auth, parts

    app.register_blueprint(auth.bp)
    app.register_blueprint(parts.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    #app.add_url_rule("/", endpoint="index")
    @app.route("/")
    def index():
        return "Hello"

    # Serve up static directory contents for datasheets
    @app.route('/data/<path:path>')
    def send_datasheet(path):
        return send_from_directory('data', path)

    return app
