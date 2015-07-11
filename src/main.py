from flask import Flask
app = Flask(__name__)
app.debug = True

@app.route('/hash/<string:population>/<string:dataset>')
def get_hash(population,dataset):
    import os
    dir = os.path.join(population, str(dataset)+".hash")
    f = open(dir)
    data = f.read()
    f.close()
    return data

@app.route('/data/<string:population>/<string:dataset>')
def get_data(population, dataset):
    import os
    dir = os.path.join(population, str(dataset)+".json")
    f = open(dir)
    data = f.read()
    f.close()
    return data

if __name__ == '__main__':
    app.run()