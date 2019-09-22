from flask import Flask, request
import json
from logfile import *
from Connection import *
import pandas as pd


app = Flask(__name__)

@app.route('/get_load_dt', methods = ['GET'])
def underload_overload_dt():
    engine = None
    logging.debug("get_load_dt function is being called!!!")
    result = {}
    try:
        division_code = request.args.get('division_code')
        division_code = division_code if division_code != "" else None

        report_type = request.args.get('report_type')
        report_type = report_type if report_type != "" else None

        month = request.args.get('month')
        month = month if month != "" else None

        year = request.args.get('year')
        year = year if year != "" else None

        if division_code is not None and month is not None and year is not None and report_type is not None:

            req_msg = "Division code is {} and month is {} and year is {} in Request".format(division_code, month, year)
            logging.debug(req_msg)

            month = month if month.isnumeric() else None
            year = year if year.isnumeric() else None
            report_type = report_type if report_type == "mrd" or report_type == "amr" else None

            if month is not None and year is not None and report_type is not None:

                engine = get_connection_from_pool()
                if engine is not None:

                    if report_type == "mrd":
                        table_name = "dt_health_report_anomoly"
                    else:
                        table_name = "amr_health_report_anomoly"

                    dt_query = "select * from master_complete where division_code='{}'".format(division_code)
                    dt_count = pd.read_sql(dt_query, con=engine)
                    result['total_dt'] = len(dt_count.index)

                    loading_query = "select T1.division_code,T1.zone_code,T1.sap_fl_location,T1.dt_code,T1.unbalanced,T1.overloaded,T1.underloaded,T2.latitude,T2.longitude" \
                                    " from (select * from {table_name} where monthh = {monthh} and " \
                                    "yearr = {yearr} and division_code='{division_code}') as T1 left join " \
                                    "(select latitude, longitude, sap_fl_location from substation) as T2 " \
                                    "on T1.sap_fl_location=T2.sap_fl_location".format(table_name=table_name, monthh=month, yearr=year, division_code=division_code)
                    loading_result = pd.read_sql(loading_query, con=engine)

                    overload_sap_fl_list = []
                    overload_final_result = {}
                    overload_final_result['sap_fl_location'] = overload_sap_fl_list
                    overload_result = loading_result[loading_result['overloaded'] == '1']

                    sql = "insert into meter_data_log(dt_sap_eqp_code,meter_no,current_r,current_y,current_b,voltage_r," \
                          "voltage_y,voltage_b,load_value,key_value,time_stamp) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"


                    overload_final_result['count'] = len(overload_result.index)
                    unique_overload_sap_fl_location = overload_result[['sap_fl_location', 'latitude', 'longitude']].drop_duplicates()
                    for index, row in unique_overload_sap_fl_location.iterrows():
                        sap_fl_dict = {}
                        sap_fl_dict['sap_fl_location'] = row['sap_fl_location']
                        sap_fl_dict['latitude'] = row['latitude']
                        sap_fl_dict['longitude'] = row['longitude']
                        overload_sap_fl_list.append(sap_fl_dict)


                    overload_final_result['sap_fl_location'] = overload_sap_fl_list
                    result['overloaded'] = overload_final_result


                else:
                    error_msg = "Server Connection Failed!!!"
                    result['error_msg'] = error_msg

            else:
                error_msg = "Month and Year should be integer and report_type should be mrd or amr"
                result['error_msg'] = error_msg

        else:
            error_msg = "Divison_code and Month and Year and Report Type(mrd, amr) are required!!!"
            logging.debug(error_msg)
            result['error_msg'] = error_msg

    except Exception as e:
        error_msg = "exception in get_load_dt:={}".format(e)
        logging.debug(error_msg)

    return result


if __name__ == "__main__":
    app.run()