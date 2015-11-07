from flask import Flask
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
    f = open(directori)
    data = f.read()
    f.close()
    return data


@app.route('/data/<string:population>/<string:dataset>')
def get_data(population, dataset):
    import os
    if 'data_dir' in app.config:
        directori = os.path.join(app.config['data_dir'], population, '{}.hash'.format(dataset))
    else:
        directori = os.path.join(population, '{}.json'.format(dataset))
    f = open(directori)
    data = f.read()
    f.close()
    return data


if __name__ == '__main__':
    config = ConfigObj('osmdata.conf')
    app.config.update(config)
    app.logger.debug(config)
    app.run(host='0.0.0.0')
