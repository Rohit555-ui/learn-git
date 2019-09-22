import time
import multiprocessing
def sqare(arr):
    for i in arr:
        time.sleep(0.2)
        print("square:", i*i)

def cube(arr):
    for i in arr:
        time.sleep(0.2)
        print("cube:", i*i*i)

t = time.time()
list1 = [1, 2, 3]
t1 = multiprocessing.Process(target = sqare, args=(list1,))
t2 = multiprocessing.Process(target = cube, args=(list1,))
t1.start()
t2.start()

t1.join()
t2.join()
print(time.time()-t)
# import logging
# logging.basicConfig(filename='x.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
#
#
# def sumf(a, b, c):
#     try:
#         log_str = "sum of {} and {} and {} is {}".format(a, b, c, a+b+c)
#         logging.info(log_str)
#         return a + b + c
#     except Exception as e:
#         logging.debug(e)
#         return "Some thing went wrong"
#
# sum_of_num = sumf(1,2,3)
# print(sum_of_num)