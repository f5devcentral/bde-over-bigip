import testlib
import requests

# socket
import socket
import random
import math
import sys
import signal
import testlib
import time
import json

def sig_handler(signum, frame):
    print("Catched signal %d\n" % signum)
    testlib.send_logs.udp_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, sig_handler)

if len(sys.argv) != 2:
    print("%s <maxps>\n" % sys.argv[0])
    sys.exit(1)

port = 20003
maxps = int(sys.argv[1])

def logging_at(ts, count):

    for n in range(0, count):
        cmd = "testlib.mock_data.mock_logging_data_%s(%d, %d)" % (port, ts, count)
        d = eval(cmd)
        print(json.dumps(d))

        resp = requests.post('http://fluentd:20003/http_input', data = json.dumps(d))
        print(resp.status_code)

        # time.sleep(0.01)
while True:
    n = int(time.time())
    count = testlib.counting.count_const(n, maxps)
    logging_at(n, count)
    time.sleep(1)

