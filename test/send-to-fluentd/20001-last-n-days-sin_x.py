import testlib

# socket
import socket
import random
import math
import sys
import time

import testlib

if len(sys.argv) != 3:
    print("%s <ndays> <maxp/s>\n" % sys.argv[0])
    sys.exit(1)

ndays = int(sys.argv[1])
maxps = int(sys.argv[2])

def connect():
    testlib.send_logs.tcp_connect('fluentd', 20001)

def logging_at(ts, count):

    for n in range(0, count):
        cmd = "testlib.mock_data.mock_logging_data_%d(%d, %d)" % (20001, ts, count)
        d = eval(cmd)
        testlib.send_logs.send_tcp(d)

    time.sleep(0.001)
connect()

(nstart, nend) = testlib.timeutils.last_n_days(ndays)
for n in range(nstart, nend):
    count = testlib.counting.count_sin(n, maxps)
    logging_at(n,count)

    if (n - nstart)* 100 % (nend - nstart) == 0:
        print("finished: %d, %d" % (int((n - nstart)* 100 / (nend - nstart)), count))

testlib.send_logs.tcp_socket.close()

