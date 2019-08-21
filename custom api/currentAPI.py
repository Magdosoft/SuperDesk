# mongo.py

import socket
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'superdesk'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/superdesk'

mongo = PyMongo(app)


@app.route('/news/<int:latestNewsIdAlreadyGot>/<int:countOfRecordsToGet>', methods=['GET'])
def get_some_news(latestNewsIdAlreadyGot,countOfRecordsToGet):

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    serverIP = s.getsockname()[0]
    s.close()
    # if request.form['password'] == 'password' and request.form['username'] == 'admin':
    news = mongo.db.ingest
    output = []

    for n in news.find({"unique_id": {"$gte": latestNewsIdAlreadyGot},"type":{"$in":["text", "picture"]}}).limit(countOfRecordsToGet):
        if n['type'] == 'text':
            output.append({'unique_id': n['unique_id'],'_created':n['_created'] , 'type':n['type'],'slugline': n['slugline'],
                       'source': n['source'], 'body_html': n['body_html']})
        elif n['type'] == 'picture':

            output.append({'unique_id': n['unique_id'],'_created':n['_created'],'type':n['type'], 'slugline': n['slugline'],
                           'source': n['source'],
                           'PhotoUri': n['renditions']['baseImage']['href'].replace('localhost',serverIP),
                           'width': n['renditions']['baseImage']['width'],
                           'height': n['renditions']['baseImage']['height'],
                           'mimetype': n['renditions']['baseImage']['mimetype']})

    return jsonify({'result': output})

@app.route('/minandmaxnewsids/', methods=['GET'])
def get_min_id():

    # if request.form['password'] == 'password' and request.form['username'] == 'admin':
    news = mongo.db.ingest
    output = []

    summary = news.aggregate([
    { "$group": {
        "_id": 1,
        "themin": { "$min": "$unique_id" },
        "themax": {"$max": "$unique_id"}
    }}
])
    for n in summary:
        minVal = n['themin']
        maxVal = n['themax']


    output.append({'min': minVal, 'max': maxVal })
    return jsonify({'result': output})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=14400)

