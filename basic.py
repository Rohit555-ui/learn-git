from flask import Flask, request
import json
import logging
from Connection import *
import pandas as pd

logging.basicConfig(filename='user_information.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
app = Flask(__name__)

@app.route('/', methods = ['GET'])
def get_data():
    return "gettting data"

def basic():
    return "basic function"

@app.route('/insertdata', methods = ['POST'])
def setdata():
    logging.debug("set data function is getting called!!!")
    try:
        my_connection = get_connection_from_pool()
        curr_obj = my_connection.cursor()
        logging.debug("setdata function called!!!")
        req_data = request.get_json()
        name = req_data['name']
        first_name = req_data['first_name']
        last_name = req_data['last_name']
        address = req_data['address']
        query = "insert into user(name,first_name,last_name,office_address) values(%s, %s, %s, %s)"
        logging.debug(query)
        val = (name, first_name, last_name, address)
        curr_obj.execute(query, val)
        my_connection.commit()
        return "Inserted Successfully"

    except Exception as e:
        exception_msg = "exception occured in setdata function is {}".format(e)
        logging.debug(exception_msg)



    return "setting"

if __name__ == "__main__":
    app.run(port='5678')