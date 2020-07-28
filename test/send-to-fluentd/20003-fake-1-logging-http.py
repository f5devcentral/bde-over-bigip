import requests
import testlib
import time

url = "http://localhost:20003/http_input"
ts = int(time.time())

log = testlib.mock_data.mock_logging_data_20003(ts, 1)

response = requests.request("POST", url, data=log)

print(log)