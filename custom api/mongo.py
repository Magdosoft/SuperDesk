# mongo.py

import socket
import httplib2
import os
from flask import Flask ,send_file
from flask import jsonify
from flask import after_this_request


#
# Hamed 21-2-2019
#
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


#
# Hamed 8-3-2019
#
import logging


from datetime import datetime, timedelta
import time
from dateutil.parser import parse
# import pandas as pd


from flask_pymongo import PyMongo
from zipfile import *
import sys

from importlib import reload 


app = Flask(__name__)

logging.basicConfig(filename='/home/newsadmin/webapi/webapi.log',level=logging.DEBUG)


limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["2 per minute", "1 per second"],
)


app.config['MONGO_DBNAME'] = 'superdesk'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/superdesk'

mongo = PyMongo(app)




#
# Hamed 21-2-2019
#
#@app.route("/ping")
#@limiter.exempt
#def ping():
#    return "PONG"


@app.route('/news/<int:latestNewsIdAlreadyGot>/<int:countOfRecordsToGet>', methods=['GET'])
# @limiter.limit("1 per 5 minute")
@limiter.exempt
def get_some_news(latestNewsIdAlreadyGot,countOfRecordsToGet):

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    serverIP = s.getsockname()[0]
    s.close()
    # if request.form['password'] == 'password' and request.form['username'] == 'admin':
    news = mongo.db.ingest
    output = []



    # Added By Hamed 10 May 2019
    # countOfRecordsToGet = 5
    # Added By Hamed 10 May 2019

    # Added By Hamed 21 May 2019
    # countOfRecordsToGet = 500
    # Added By Hamed 21 May 2019

    # Added By Hamed 3 June 2019
    countOfRecordsToGet = 50
    # Added By Hamed 3 June 2019



    results = news.find({"unique_id": {"$gte": latestNewsIdAlreadyGot},"type":{"$in":["text", "picture"]}}).limit(countOfRecordsToGet)

    for n in results:
        if n['type'] == 'text':
              # print("text text text text text text text text text text text text text")
              output.append({'unique_id': n['unique_id'], '_created': n['_created'], 'type': n['type'], 'headline': n.get('headline','---'),
                       'source': n['source'], 'body_html': n['body_html']})

        elif n['type'] == 'picture':
              # https://docs.quantifiedcode.com/python-anti-patterns/correctness/not_using_get_to_return_a_default_value_from_a_dictionary.html
              output.append({'unique_id': n['unique_id'], '_created': n['_created'], 'type': n['type'], 'headline': n.get('headline','---'),
                           'caption': n.get('description_text', '---'),
                           'source': n['source'],
                           'PhotoUri': n['renditions']['original']['href'].replace('localhost',serverIP),
                           'width': n['renditions']['baseImage']['width'],
                           'height': n['renditions']['baseImage']['height'],
                           'mimetype': n['renditions']['baseImage']['mimetype']})

    return jsonify({'result': output})


@app.route('/minandmaxnewsids/', methods=['GET'])
@limiter.limit("1 per 5 minute")
def get_min_max_ids():

    # if request.form['password'] == 'password' and request.form['username'] == 'admin':
    news = mongo.db.ingest
    output = []

    summary = news.aggregate([
        { "$match":  {"type": { "$in":["text", "picture"]}}},
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




@app.route('/DownloadItemAsZip/<int:ItemUniqueId>', methods=['GET'])
@limiter.exempt
def download_item_as_zip(ItemUniqueId):
    reload(sys)
    # sys.setdefaultencoding('utf-8')

    file_name = "ToBedownload.zip"
    zip_archive = ZipFile(file_name, "w")

    news = mongo.db.archive


    results = news.find({"unique_id": {"$eq": ItemUniqueId}})

    for n in results:
        if n['type'] == 'text':
            with open(str(n['unique_id']) + " - " + str(n['source']) + ".html", 'wb') as f:
                f.write("<h1>"+ n['headline'] +"</h1>" + "<h5>" + n['source'] + " - "  + str(n['_created']) +"</h5>"+
                        n['body_html'])
            zip_archive.write(str(n['unique_id']) + " - " + str(n['source']) + ".html")
            os.remove(str(n['unique_id']) + " - " + str(n['source']) + ".html")

        elif n['type'] == 'picture':
            resp, content = httplib2.Http().request(n['renditions']['original']['href'])
            with open( str(n['unique_id']) +  " - " + str(n['source']) + ".jpg" , 'wb') as f:
                f.write(content)
            # return jsonify({'result': output})
            zip_archive.write(str(n['unique_id']) +  " - " + str(n['source']) + ".jpg")
            os.remove(str(n['unique_id']) +  " - " + str(n['source']) + ".jpg")

        elif n['type'] == 'composite':
            counter = 0
            for item in n['groups'][1]['refs']:
                counter = counter + 1
                resp, content = httplib2.Http().request(item['renditions']['original']['href'])
                with open("image" +str(counter) + ".jpg", 'wb') as f:
                    f.write(content)
                zip_archive.write("image" +str(counter) + ".jpg")
                os.remove("image" +str(counter) + ".jpg")
    zip_archive.close()

    @after_this_request
    def remove_file(response):
        try:
            os.remove("ToBedownload.zip")
            # file_handle.close()
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response
    return send_file("ToBedownload.zip")



if __name__ == '__main__':
    app.run(debug=True,threaded=True, host='0.0.0.0', port=14400)

