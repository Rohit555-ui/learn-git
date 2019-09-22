from flask import Flask, request
import requests
from flask1 import *
import json
import pandas as pd
# from logging import *
import logging
#logging module of python not flask and FileHandler is a class


app = Flask(__name__)

# file_handler = FileHandler('error.log')#path and name of file which will be created automatecally
# file_handler.setLevel(WARNING)
# app.logger.addHandler(file_handler)

logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

@app.route('/getuserdata', methods = ['POST'])
def getdata():
    reqData = request.get_json()
    myConnection = get_connection_from_pool()
    object = myConnection.cursor()

    if "name" in reqData:
        name = reqData['name']
        first_name = reqData['first_name']
        last_name = reqData['last_name']
        address = reqData['address']
        return "present"
    else:
        return "not"

    # val = (name, first_name, last_name, address)
    # data = object.execute("insert into user(name,first_name,last_name,office_address) values(%s,%s,%s,%s)", val)
    # myConnection.commit()
    # object.close()
    # if(data):
    #     return "saved successfully"
    # else:
    #     return "not saved"


@app.route('/updatedata', methods = ['PUT'])
def updatedata():
    name = request.get_json('name')
    check = {}
    check['name'] = name['name']
    check['address'] = name['address']
    return json.dumps(check)


@app.route('/insertdata', methods = ['GET'])
def insertdata():
    name = "test_name"
    address = "test_address"
    first_name = "test_first_name"
    last_name = "test_last_name"
    myConnection = get_connection_from_pool()
    curr_diff = myConnection.cursor()
    check = {}
    insert_query = "insert into user(name,first_name,last_name,office_address) values(%s,%s,%s,%s)"
    val = (name, address, first_name, last_name)
    check['query'] = insert_query
    curr_diff.execute(insert_query, val)
    myConnection.commit()
    curr_diff.close()

    return json.dumps(check)


@app.route('/get_meter_reader_status', methods = ['GET'])
def get_meter_reader_status():
    result = {}
    month = request.args.get('month')
    year = request.args.get('year')
    type = request.args.get('type')
    result['month'] = month
    result['year'] = year
    result['type'] = type
    logging.debug(result)
    # a = 1 / 0
    # result['value'] = a
    return json.dumps(result)




if __name__ == "__main__":
    app.run()