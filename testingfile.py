import schedule
import time

# def fun():
#     print("function is calling again and again")
#
# print("running successfully!!!")
#
# schedule.every(5).seconds.do(fun) it calls fun function after every 5 seconds
#
#
# while 1:
#     schedule.run_pending()
#     time.sleep(1)

def sqr(list2):
    for i in list2:
        time.sleep(1)
        print(i*i)

list1 = [1, 2, 3, 4, 5]

sqr(list1)