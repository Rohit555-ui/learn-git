from flask import Flask, request
from flask1 import *
import pandas as pd
import json


def getMeterDayWiseSummary(user_name,month,year,engine):
    user_id_query = "select id from user where name='"+user_name+"'"
    user_id_result = pd.read_sql_query(user_id_query,engine)
    user_id = str(user_id_result.loc[0]['id'])

    all_data_query = "select * from meter_reader_dt_mapping where monthh='"+str(monthh)+"' and yearr='"+str(yearr)+"' and assigned_user_id='"+str(user_id)+"'"
    all_data = pd.read_sql_query(all_data_query,engine)

    
