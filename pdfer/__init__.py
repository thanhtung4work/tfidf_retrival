import os

from   flask import Flask, render_template
from   prometheus_flask_exporter import PrometheusMetrics

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    metrics = PrometheusMetrics(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    from .blueprint import extract
    from .blueprint import documents

    app.register_blueprint(extract.bp)
    app.register_blueprint(documents.bp)

    @app.route("/")
    def index():
        return render_template("upload.html")

    return app