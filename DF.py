from flask1 import *
import sys
import pandas as pd


name = sys.argv[1]
address = sys.argv[2]
marks = sys.argv[3]

myConnection = get_connection_from_pool()
curr_diff = myConnection.cursor()
check = {}
insert_query = "insert into student(name,address,marks) values(%s,%s,%s)"
val = (name, address, marks)
check['query'] = insert_query
curr_diff.execute(insert_query, val)
myConnection.commit()
curr_diff.close()



# data = [['a',22,10000],['b',23,11000],['c',24,12000],['d',25,13000],['e',26,20000],['f',27,25000]]
#
# DF = pd.DataFrame(data,columns=['Name','Age','Salary'])
# age_list = []
# for i in DF.Age:
#     if i > 23:
#         age_list.append("true")
#     else:
#         age_list.append("false")
#
# first_two = DF.loc[DF.Age > 23]
# print(first_two)