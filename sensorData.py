from flask import Flask, request
from flask1 import *
from base_functions import *
import pandas as pd
import json,calendar


app = Flask(__name__)

@app.route("/see")
def movie():
	return "article"


@app.route("/get_all_loads", )
def get_all_loads():
	result = {}
	result['overload'] = {}
	result['underload'] = {}
	result['unbalance'] = {}

	overload_sap_fl_details = []
	underload_sap_fl_details = []
	unbalance_sap_fl_details = []
	engine = get_engine_from_pool()
	req_data = request.get_json()
	month = req_data['month']
	year = req_data['year']
	div_code = req_data['div_code']
	query = "select * from dt_health_report_anomoly where monthh="+str(month)+" and yearr="+str(year)+" and division_code="+str(div_code)
	all_dt_code = pd.read_sql_query(query, engine)

	overload_df = all_dt_code[all_dt_code['overloaded'] == '1']
	underload_df = all_dt_code[all_dt_code['underloaded'] == '1']
	unbalance_df = all_dt_code[all_dt_code['unbalanced'] == '1']

	overload_sap_fl_detail = "SELECT T.sap_fl_location AS sap_location,overloaded,underloaded,unbalanced,(SELECT latitude FROM substation WHERE sap_fl_location = sap_location) AS latitude,(SELECT longitude FROM substation WHERE sap_fl_location = sap_location) AS longitude FROM (SELECT distinct(sap_fl_location) as sap_fl_location,overloaded,underloaded,unbalanced FROM dt_health_report_anomoly WHERE overloaded='1' and division_code ="+str(div_code)+" AND monthh ="+str(month)+" AND yearr ="+str(year)+") as T"
	overload_sap_fl_result = pd.read_sql_query(overload_sap_fl_detail,engine)
	underload_sap_fl_detail = "SELECT T.sap_fl_location AS sap_location,overloaded,underloaded,unbalanced,(SELECT latitude FROM substation WHERE sap_fl_location = sap_location) AS latitude,(SELECT longitude FROM substation WHERE sap_fl_location = sap_location) AS longitude FROM (SELECT distinct(sap_fl_location) as sap_fl_location,overloaded,underloaded,unbalanced FROM dt_health_report_anomoly WHERE underloaded='1' and division_code ="+str(div_code)+" AND monthh ="+str(month)+" AND yearr ="+str(year)+") as T"
	underload_sap_fl_result = pd.read_sql_query(underload_sap_fl_detail,engine)
	unbalanced_sap_fl_detail = "SELECT T.sap_fl_location AS sap_location,overloaded,underloaded,unbalanced,(SELECT latitude FROM substation WHERE sap_fl_location = sap_location) AS latitude,(SELECT longitude FROM substation WHERE sap_fl_location = sap_location) AS longitude FROM (SELECT distinct(sap_fl_location) as sap_fl_location,overloaded,underloaded,unbalanced FROM dt_health_report_anomoly WHERE unbalanced='1' and division_code ="+str(div_code)+" AND monthh ="+str(month)+" AND yearr ="+str(year)+") as T"
	unbalanced_sap_fl_result = pd.read_sql_query(unbalanced_sap_fl_detail,engine)


	result['overload']['count'] = len(overload_df.index)
	result['overload']['sap_fl_location'] = overload_sap_fl_details
	for i in range(len(overload_sap_fl_result.index)):
		overload_details = {}
		overload_details['sap_fl_location'] = overload_sap_fl_result.loc[i]['sap_location']
		overload_details['latitude'] = overload_sap_fl_result.loc[i]['latitude']
		overload_details['longitude'] = overload_sap_fl_result.loc[i]['longitude']
		overload_sap_fl_details.append(overload_details)
	result['overload']['sap_fl_location'] = overload_sap_fl_details


	result['underload']['count'] = len(underload_df.index)
	result['underload']['sap_fl_location'] = underload_sap_fl_details
	for i in range(len(underload_sap_fl_result.index)):
		underload_details = {}
		underload_details['sap_fl_location'] = underload_sap_fl_result.loc[i]['sap_location']
		underload_details['latitude'] = underload_sap_fl_result.loc[i]['latitude']
		underload_details['longitude'] = underload_sap_fl_result.loc[i]['longitude']
		underload_sap_fl_details.append(underload_details)
	result['underload']['sap_fl_location'] = underload_sap_fl_details


	result['unbalance']['count'] = len(unbalance_df.index)
	result['unbalance']['sap_fl_location'] = unbalance_sap_fl_details
	for i in range(len(unbalanced_sap_fl_result.index)):
		unbalance_details = {}
		unbalance_details['sap_fl_location'] = unbalanced_sap_fl_result.loc[i]['sap_location']
		unbalance_details['latitude'] = unbalanced_sap_fl_result.loc[i]['latitude']
		unbalance_details['longitude'] = unbalanced_sap_fl_result.loc[i]['longitude']
		unbalance_sap_fl_details.append(unbalance_details)
	result['unbalance']['sap_fl_location'] = unbalance_sap_fl_details

	return json.dumps(result)


@app.route("/getMeterSummary")
def getMeterSummary():
	user_name = request.args.get('user_name')
	month = request.args.get('month')
	year = request.args.get('year')
	engine = get_engine_from_pool()

	result = "gtg"
	return result


@app.route("/getSensorData", methods=['GET'])
def getData():
	result = {}
	underload_dt_list = []
	overload_dt_list = []
	unbal_dt_list = []

	zone_code = request.args.get('zone_code')
	month = request.args.get('month')
	year = request.args.get('year')
	engine = get_engine_from_pool()
	
	underload_dt_count_query = "select * from dt_health_report_anomoly where zone_code='"+zone_code+"' and monthh="+month+" and yearr="+year+" and underloaded=1"
	underload_dt_data = pd.read_sql_query(underload_dt_count_query,engine)
	underload_dt_count = len(underload_dt_data.index)

	overload_dt_count_query = "select * from dt_health_report_anomoly where zone_code='"+zone_code+"' and monthh="+month+" and yearr="+year+" and overloaded=1"
	overload_dt_data = pd.read_sql_query(overload_dt_count_query,engine)
	overload_dt_count = len(overload_dt_data.index)

	unbal_dt_count_query = "select * from dt_health_report_anomoly where zone_code='"+zone_code+"' and monthh="+month+" and yearr="+year+" and unbalanced=1"
	unbal_dt_data = pd.read_sql_query(unbal_dt_count_query,engine)
	unbal_dt_count = len(unbal_dt_data.index)

	result['zone_code'] = zone_code
	result['month'] = month
	result['year'] = year
	result['underloaded'] = underload_dt_list
	result['overloaded'] = overload_dt_list
	result['unbalanced'] = unbal_dt_list

	for i in range(underload_dt_count):
		underload_dt_list_data = {}
		underload_dt_list_data['dt_code'] = underload_dt_data.loc[i]['dt_code']
		underload_dt_list_data['sap_fl_location'] = underload_dt_data.loc[i]['sap_fl_location']
		underload_dt_list.append(underload_dt_list_data)

	for i in range(overload_dt_count):
		overload_dt_list_data = {}
		overload_dt_list_data['dt_code'] = overload_dt_data.loc[i]['dt_code']
		overload_dt_list_data['sap_fl_location'] = overload_dt_data.loc[i]['sap_fl_location']
		overload_dt_list.append(overload_dt_list_data)

	for i in range(unbal_dt_count):
		unbal_dt_list_data = {}
		unbal_dt_list_data['dt_code'] = unbal_dt_data.loc[i]['dt_code']
		unbal_dt_list_data['sap_fl_location'] = unbal_dt_data.loc[i]['sap_fl_location']
		unbal_dt_list.append(unbal_dt_list_data)


	return json.dumps(result)
	
@app.route("/getSubMaster", methods=['GET'])
def getSubMaster():
	sap_fl_location = request.args.get('sap_fl_location')
	engine = get_engine_from_pool()
	dt_list = []
	query = "select D.division_name,Z.zone_name from division D inner join zone Z on D.id = Z.division_id inner join substation S on S.zone_id=Z.id where S.sap_fl_location='"+sap_fl_location+"'";
	master_result = pd.read_sql_query(query,engine)

	dt_query = "select dt_code from dt where substation_id in(select id from substation where sap_fl_location='"+sap_fl_location+"')"
	dt_result = pd.read_sql_query(dt_query,engine)

	result = {}
	for i in range(len(master_result.index)):
		result['division_name'] = str(master_result.loc[i]['division_name'])
		result['zone_name'] = str(master_result.loc[i]['zone_name'])
	result['dt'] = dt_list
	for i in range(len(dt_result.index)):
		list_of_dt = {}
		list_of_dt['dt_code'] = str(dt_result.loc[i]['dt_code'])
		dt_list.append(list_of_dt)

	result['dt'] = dt_list

	return json.dumps(result)

@app.route('/getMeterSummaryDayWise', methods=['GET'])
def getMeterSummaryDayWise():
	month = request.args.get('month')
	year = request.args.get('year')
	user_name = request.args.get('user_name')
	engine = get_engine_from_pool()
	user_id_query = "select id from user where name='"+str(user_name)+"'"
	user_id_result = pd.read_sql_query(user_id_query, engine)
	result = {}
	usr_id = int(user_id_result.loc[0]['id'])

	assigned_count_query = "select * from meter_reader_dt_mapping where monthh="+str(month)+" and yearr="+str(year)+" and assigned_user_id="+str(usr_id)
	assigned_count_result = pd.read_sql_query(assigned_count_query, engine)
	assigned_count = len(assigned_count_result.index)
	# result['query'] = assigned_count_query
	# result['count'] = assigned_count
	day_list = []
	no_of_days = calendar.monthrange(int(year), int(month))[1]
	result['day'] = no_of_days
	result['day_wise_list'] = day_list
	for i in range(1, no_of_days+1):
		day_details = {}
		day_details['day'] = i
		day_list.append(day_details)
		date_format = str(year).zfill(2)+"-"+str(month).zfill(2)+"-"+str(i).zfill(2);

		date_wise_df = assigned_count_result[assigned_count_result['time_stamp'].str.contains(date_format)]

		start_time = str(year)+"-"+str(month)+"-"+str(i)+" 00:00:00"
		end_time = str(year)+"-"+str(month)+"-"+str(i)+" 23:59:59"
		#date_wise_df = assigned_count_result.loc[(assigned_count_result['time_stamp'] > start_time) & (assigned_count_result['time_stamp'] < end_time)]

		download_df = date_wise_df.loc[date_wise_df['current_status'] == 'reading_done']
		not_download_df = date_wise_df.loc[date_wise_df['current_status'] == 'not_reading']

		day_details['date'] = date_format
		day_details['assigned'] = assigned_count
		day_details['download'] = len(download_df.index)
		day_details['not_download'] = len(not_download_df.index)
	result['day_wise_list'] = day_list
	return json.dumps(result)


if __name__ == "__main__":
    app.run()