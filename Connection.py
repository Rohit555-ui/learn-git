import pymysql
from sqlalchemy import create_engine

from logfile import *

def get_engine_from_pool():
	engine = None()
	try:
		engine = create_engine('mysql+pymysql://probusdev:probusdev@rdscopy3.cea15vlld93o.us-east-1.rds.amazonaws.com/sense')
	except Exception as e:
		logging.debug("get_engine" + str(e))
	return engine

def get_connection_from_pool():
	connection = None
	try:
		connection = pymysql.connect(host='rdscopy3.cea15vlld93o.us-east-1.rds.amazonaws.com', user='probusdev',
                                   passwd='probusdev', db='sense')
	except Exception as e:
		logging.debug("get_connection" + str(e))
	return connection


# curr_diff = myConnection.cursor()
# curr_diff.execute(insert_query)
# 	myConnection.commit()
# 	curr_diff.close()