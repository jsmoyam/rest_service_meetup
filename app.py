#!flask/bin/python

from flask import Flask, request, abort, jsonify
from tools import Log, log_entry
import httplib2
import random

app = Flask(__name__)
log = Log().get_log()


def send_get_request(url):
    http = httplib2.Http()
    response, content = http.request(url, 'GET')
    return content

@app.route('/info_planet', methods=['GET'])
@log_entry()
def info_planet():
    ''' curl -i -X GET http://localhost:5000/info_planet '''

    planet = random.randrange(10)
    response = send_get_request('https://swapi.co/api/planets/%s/' % planet)

    return response

if __name__ == '__main__':
    app.run(debug=True)
