from flask import Flask, abort, Response
from flask.ext.cors import CORS

from configobj import ConfigObj

app = Flask(__name__)
CORS(app)
app.debug = True


@app.route('/hash/<string:population>/<string:dataset>')
def get_hash(population, dataset):
    import os
    if 'data_dir' in app.config:
        directori = os.path.join(app.config['data_dir'], population, '{}.hash'.format(dataset))
    else:
        directori = os.path.join(population, '{}.hash'.format(dataset))
    if os.path.isfile(directori):
        f = open(directori)
        data = f.read()
        f.close()
        return data
    else:
        abort(404)



@app.route('/data/<string:population>/<string:dataset>.json')
def get_data(population, dataset):
    import os
    if 'data_dir' in app.config:
        directori = os.path.join(app.config['data_dir'], population, '{}.json'.format(dataset))
    else:
        directori = os.path.join(population, '{}.json'.format(dataset))
    app.logger.debug(directori)
    if os.path.isfile(directori):
        f = open(directori)
        data = '['+f.read()+']'
        f.close()
        resp = Response(response=data, status=200, content_type='text/plain; charset=utf-8')
        return resp
    else:
        abort(404)


if __name__ == '__main__':
    config = ConfigObj('osmdata.conf')
    app.config.update(config)
    app.run(host='0.0.0.0', port=8080)
