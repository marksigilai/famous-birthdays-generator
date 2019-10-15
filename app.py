#!flask/bin/python
import sys
import re
import datetime, calendar
import os
import requests
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
from html.parser import HTMLParser
from flask import Flask, jsonify, make_response, request, abort, render_template, g
from bs4 import BeautifulSoup



app = Flask(__name__)
authorized_tokens = {}


@app.route('/')
def load_page():
    return render_template('main.html')


@app.route('/', methods=['GET'])
def static_logs():
    return render_template('main.html')


@app.route('/submit', methods=['POST', 'GET'])
def render_date():
    date = request.args.get('date')
    print(date)
    err = 'yes'
    if date:
        err = 'no'
        datestr = make_date(date)
        response = scrape(datestr)
        resp = response[::-1]
        return render_template('main.html', result = resp, error = err)
    return render_template('main.html', error = err)

def scrape(date):
    url = "https://en.wikipedia.org/wiki/" + date
    print(url)
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    famouslist = soup.find('div', attrs={'class': 'mw-parser-output'}).find_all('ul')[2]
    t = famouslist.get_text()
    tt = t.split("\n")
    ttt = []
    for i in range(len(tt)):
        if re.match('19.*', tt[i]):
            ttt.append(tt[i])
    return ttt


def make_date(dateNum):
    if not dateNum:
        return
    else:
        arrnum = dateNum.split("-")
        montharr = calendar.month_name
        daynum = arrnum[2]
        monthstr = montharr[int(arrnum[1])]
        datestr = (monthstr + "_" + daynum)
        return datestr


@app.errorhandler(400)
def bad_request(error):
    """ Respond to bad request """
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(401)
def not_authorized(error):
    """ Respond to non-authorized request """
    return make_response(jsonify({'error': 'Not Authorized'}), 401)


@app.errorhandler(404)
def not_found(error):
    """ Respond to unfound request """
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(405)
def not_allowed(error):
    """ Respond to disallowed request """
    return make_response(jsonify({'error': 'Not allowed'}), 405)



@app.template_filter('dt')
def filter_datetime(date, fmt=None):
    date = date + (datetime.datetime.now() - datetime.datetime.utcnow())
    return date.strftime("%Y/%m/%d %H:%M:%S")


if __name__ == '__main__':
    print("\n+ Setting up app prerequisites..")
    print("+ Setup Complete\n")
    # Run app
    app.run(debug=False, host='localhost', port=8080)
