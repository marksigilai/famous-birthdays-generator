#!flask/bin/python
import sys
import re
import datetime, calendar
import os
import requests
import json
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
from flask import Flask, jsonify, make_response, request, abort, render_template, g
from bs4 import BeautifulSoup
from people import person


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
        #response = []
        #response.append(person("mr mark sigi", 1999, "Mys"))
        #response.append(person("mr  sigi", 1299, "UNKNOWN"))
        #response.append(person("  sigi", 1499, "Myers"))
        #response.append(person("mr  ", 1939, "UNKNsadfamncn dsfg sdfg dfsg sdf g sdfg d aesr  rt ghfj d sOWN"))

        print(response[len(response) - 2].to_string())
        return render_template('main.html', result = response[::-1], error = err)
    return render_template('main.html', error = err)

def createList(famous_list):
    all_people = []

    for i in range(len(famous_list)):

        split_spaces = re.split('   |, |  | ', famous_list[i])
        split_comma = re.split(',', famous_list[i])
        split_capitals = re.findall('[A-Z]\w+', split_comma[0])
        print(split_comma)
        birthdate = split_spaces[0]
        try:
            name = split_capitals[0]
            for z in range(len(split_capitals) - 1):
                z += 1
            name += ' ' + split_capitals[z]
        except Exception:
            name = re.findall('[a-zA-Z].*', split_comma[0])
            print("Special Name is ----------------------------------------------------------------------->  " + name[0])

        try:
            information = split_comma[1]
        except Exception:
            information = 'No information on this person'

        all_people.append(person(name,birthdate,information))
        print(all_people[i].get_information())

    sorted_list = set_index(all_people)
    return sorted_list

def set_index(list):
    for i in range(len(list)):
        print(list[i].get_name())
        try:
            name = list[i].get_name().split()
            formatted_name = name[0]
            print(name)
        except Exception:
            continue

        for k in range(len(name)-1):
            k = k + 1
            formatted_name += '_' + name[k]

        print(formatted_name)
        #url = "https://tools.wmflabs.org/pageviews/?project=en.wikipedia.org&platform=all-access&agent=user&range=all-time&pages=" + formatted_name
        url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/"+ formatted_name + "/monthly/2015070100/2019112000"
        try:
            response = requests.get(url).json()
            total_views = 0
            for resp in response['items']:
                total_views += resp['views']
            print(total_views)
            list[i].set_index(total_views)
            print(list[i].get_name() + "  " + str(list[i].get_index()))
        except Exception:
            list[i].set_index(0)
            print("No Link found for this person")

    quicksort(list, 0, len(list) - 1)
    return list

def quicksort_partition(list, low, high):
    i = ( low-1 )         # index of smaller element
    pivot = list[high].get_index()    # pivot

    for j in range(low , high):
        # If current element is smaller than the pivot
        if   list[j].get_index() < pivot:
            # increment index of smaller element
            i = i+1
            list[i],list[j] = list[j],list[i]
    list[i+1],list[high] = list[high],list[i+1]
    return i+1

def quicksort(list, low, high):
    if low < high:
        # pi is partitioning index, arr[p] is now
        # at right place
        pi = quicksort_partition(list,low,high)
        # Separately sort elements before
        # partition and after partition
        quicksort(list, low, pi-1)
        quicksort(list, pi+1, high)

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

    return createList(ttt)


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
