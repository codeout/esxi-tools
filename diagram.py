from flask import Flask, Response
import os

from inet_henge.models import Dumper
import esxi


def flask():
    app = Flask(__name__)
    options, args = esxi.parse_options()

    @app.route('/data')
    def data():
        client = esxi.Client(host=options.host, user=options.user, password=options.password)
        return Response(Dumper(client).dump(), mimetype='application/json')

    return app


if __name__ == '__main__':
    app = flask()
    app.run(debug=os.getenv('DEBUG', 'False') != 'False')
