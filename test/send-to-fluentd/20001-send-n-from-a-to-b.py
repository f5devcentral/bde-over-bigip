import testlib

# socket
import socket
import random
import math
import sys
import time

import testlib

if len(sys.argv) != 4:
    print("%s <maxps> <start-timestr> <end-timestr>\n" % sys.argv[0])
    sys.exit(1)

port = 20001
maxps = int(sys.argv[1])
start = sys.argv[2]
end = sys.argv[3]

def connect():
    testlib.send_logs.tcp_connect('fluentd', port)

def logging_at(ts, count):

    for n in range(0, count):
        cmd = "testlib.mock_data.mock_logging_data_%s(%d, %d)" % (port, ts, count)
        d = eval(cmd)
        testlib.send_logs.send_tcp(d)

        # time.sleep(0.01)

connect()

(nstart, nend) = (testlib.timeutils.str2ts(start), testlib.timeutils.str2ts(end))
for n in range(nstart, nend):
    count = testlib.counting.count_const(n, maxps)
    if (n - nstart)* 100 % (nend - nstart) == 0:
        print("finished: %d, %d" % (int((n - nstart)* 100 / (nend - nstart)), count))
    logging_at(n,count)

testlib.send_logs.tcp_socket.close()

