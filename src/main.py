from flask import Flask, abort
from configobj import ConfigObj

app = Flask(__name__)
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
    else:
        abort(404)
    return data


@app.route('/data/<string:population>/<string:dataset>')
def get_data(population, dataset):
    import os
    if 'data_dir' in app.config:
        directori = os.path.join(app.config['data_dir'], population, '{}.json'.format(dataset))
    else:
        directori = os.path.join(population, '{}.json'.format(dataset))
    app.logger.debug(directori)
    if os.path.isfile(directori):

        f = open(directori)
        data = f.read()
        f.close()
    else:
        abort(404)
    return data


if __name__ == '__main__':
    config = ConfigObj('osmdata.conf')
    app.config.update(config)
    app.logger.debug(config)
    app.run(host='0.0.0.0')
