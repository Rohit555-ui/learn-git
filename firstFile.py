import logging

logging.basicConfig(filename='logTesting.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def sum(a, b):
    logging.debug(a+b)
    return a+b

v1 = 10
v2 = 20
value_msg = "value1:= {} and value2:= {} before sum".format(v1, v2)
logging.debug(value_msg)
a = sum(v1, v2)
logging.error(a)

print(a)

print("master1")