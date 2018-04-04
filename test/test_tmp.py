import datetime
import time
import json


def test_timestamp():
    list_date = []
    for i in range(10):
        list_date.append(datetime.datetime.now().timestamp());
    print(list_date)
    list_date.sort()
    print(list_date)
    list_nice = []
    for t in list_date:
        list_nice.append(datetime.datetime.utcfromtimestamp(t))
    print(list_nice)

    str_list_date = json.dumps(list_date)
    print("str_list_date: " + str_list_date)
    list_decode = json.loads(str_list_date)
    print(list_decode)
    print('---------------')
    for d in list_decode:
        print(datetime.datetime.utcfromtimestamp(d))


if __name__ == '__main__':
    pass
