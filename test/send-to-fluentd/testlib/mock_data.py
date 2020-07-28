import random
import timeutils
import json
import uuid

RESPCODES = [200, 200, 200, 200, 200, 200, 202, 202, 204, 204, 400, 401, 404, 410, 500, 503]
MAXCOUNT = 4000

def mock_logging_data_8083(ts, concurrency):
    size = random.randint(1, 1024)
    resp_code = RESPCODES[random.randint(0, len(RESPCODES)-1)]
    latency = random.randint(1, 5)
    latency = latency * 2 if size > 128 else latency
    latency = latency * 4 if concurrency > MAXCOUNT/2 else latency * 2 if concurrency > MAXCOUNT/4 else latency

    logdata = "%s: %d %d %d" %(timeutils.ts2str(ts), latency, size, resp_code)

    return logdata

def mock_logging_data_8084(ts, concurrency):
    size = random.randint(1, 1024)
    resp_code = RESPCODES[random.randint(0, len(RESPCODES)-1)]
    latency = random.randint(1, 5)
    latency = latency * 2 if size > 128 else latency
    latency = latency * 4 if concurrency > MAXCOUNT/2 else latency * 2 if concurrency > MAXCOUNT/4 else latency

    logdata = "%s: %d %d %d" %(timeutils.ts2str(ts), latency, size, resp_code)

    return logdata

USER_AGENTS = (
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7_0; en-US)",
    "AppleWebKit/534.21 (KHTML, like Gecko) Chrome/11.0.678.0 Safari/534.21",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:0.9.2)",
    "Gecko/20020508 Netscape6/6.1",
    "Mozilla/5.0 (X11;U; Linux i686; en-GB; rv:1.9.1)",
    "Gecko/20090624 Ubuntu/9.04 (jaunty) Firefox/3.5",
    "Opera/9.80 (X11; U; Linux i686; en-US; rv:1.9.2.3) Presto/2.2.15 Version/10.10"
)

SOURCES = ['.'.join((str(random.randint(1,254)) for _ in range(4))) for _ in range(100)]
DESTINATIONS = ['10.250.11.37', '10.250.11.24', '10.250.11.99', '10.250.11.37', '10.250.11.37']
# print([10, 172, 192] + range(224, 256) )
for n in SOURCES:
    for m in [10, 172, 192 ] + range(224, 256):
        if n.startswith("%d." % m):
            # print("removing %s" % n)
            SOURCES.remove(n)

USERNAMES = [
    'zongzw', 'andrew', 'andrewzong', 'zongzhaowei', 'kk', 'zz', 'xiong', 'zongzi', 'zong', 'zong',
    'sally', 'annie'
]

METHODS = [
    'GET', 'POST', 'DELETE', 'PUT', 'PATCH', 'GET', 'POST', 'PUT', 'GET'
]

URIS = {
    '/index.html': {'size': 4353},
    '/pages/344': {'size': 344},
    '/images': {'size': 451024},
    '/': {'size': 45},
    '/gsts.tar.gz': {'size': 2*1024*1024},
    '/p/c8edab99173d': {'size': 2254},
    '/search': {'size': 4321},
    '/index.html': {'size': 53243},
    '/': {'size': 23434},
    '/search': {'size': 2334}
}

PORTS = [56002, 34563, 34345, 33746, 3344, 23345]

QNAMES = [
    'www.baidu.com',
    'httrack.website.com.cn',
    'google.com',
    'www.myf5.net'
]

def mock_logging_data_20001(ts, concurrency):
    #{
    # "timestamp": "$DATE_YYYY-$DATE_MM-${DATE_DD}T${TIME_HMS}.000Z", 
    # "client-ip": "${X-Forwarded-For}", 
    # "host": "$Host", 
    # "user-agent": "${User-agent}", 
    # "cookie": "$Cookie", 
    # "method": "$HTTP_METHOD", 
    # "uri": "$HTTP_URI", 
    # "username": "$Username", 
    # "content-type": "${Content-Type}", 
    # "server-ip": "$SERVER_IP", 
    # "latency": $RESPONSE_MSECS, 
    # "status": "$HTTP_STATCODE", 
    # "sender": "zongzw"
    # }

    rand_src = random.choice(SOURCES)
    user_agent = random.choice(USER_AGENTS)
    rand_dest = random.choice(DESTINATIONS)
    uri = random.choice(URIS.keys())
    jdata = {
        "timestamp": timeutils.ts2str(ts),
        "client-ip": rand_src,
        # "client-ip": "10.250.11.24",
        "host": "bigip-vs-server",
        "user-agent": user_agent,
        "cookie": "",
        "method": random.choice(METHODS),
        "uri": uri,
        "username": random.choice(USERNAMES),
        "content-type": "application/json",
        "server-ip": rand_dest,
        "latency": random.randint(1, 20),
        "resp-status": random.choice(RESPCODES),
        "sender": "zongzw %0d" % random.randint(0, 100),
        "stdout": "OK",

        'vs_name': random.choice(['/Common/vs-l4-84', '/Common/vs-l7-80']),
        'client_remote_port': random.choice([56002, 34563, 34345, 33746, 3344, 23345]),
        'client_local': 'bigip-clientside-ip',
        'server_local': 'bigip-serverside-ip',
        'server_local_port': random.choice([84, 80]),
        'server_remote': rand_dest,
        'server_remote_port': random.choice([84, 80]),
        'delay_type': random.choice(['svr-pkts-delay', 'init-delay', 'HS-delay']),
        'delay_value': random.randint(1, 10),
        'cdnumber': random.randint(1, 4),

        'transmission': {
            'resource_size': URIS[uri]['size'],
            'resource_name': uri
        }
    }
    
    return json.dumps(jdata)

HOSTNAMES = ['8bc234-245dacd.bigip.local', '58db82ad-2452badd.bigip.local']
def mock_logging_data_20002(ts, concurrency):

    rand_src = random.choice(SOURCES)
    user_agent = random.choice(USER_AGENTS)
    rand_dest = random.choice(DESTINATIONS)
    jdata = {
        "timestamp": timeutils.ts2str(ts),
        "clientip": rand_src,
        'clientport': random.choice(PORTS),
        'queryid': "%x" % random.randint(0, 100000),
        'origin': random.choice(QNAMES),
        'status': random.choice(['OK', 'FAILED']),
        "user-agent": user_agent,
        
        "stdout": "OK"
    }

    def rand_request():
        d = {
            "data_type": 'request',
            "F5hostname": random.choice(HOSTNAMES),
            "viewname": random.choice(['aaa', 'bbb', 'none', 'none']),
            'listenervs': rand_dest,
            'queryname': random.choice(QNAMES),
            'querytype': random.choice(['A', 'AAAA', 'MX']),
            'routedomain': random.randint(1, 10)
        }
        return d

    def rand_response():
        d = {
            "data_type": 'response',
            "F5Reponsehostname": random.choice(HOSTNAMES),
            "responsecode": random.choice(['OK', 'FAILED']),
            "responseflag": random.choice(['what', 'is', 'a', 'flag', 'qr']),
            'responsename': random.choice(HOSTNAMES),
            'answer': random.choice(SOURCES)
        }

        if random.randint(0, 10) > 5: 
            d['emptyresponse'] = 'yes' 
        if random.randint(0, 10) > 5:
            d['iswideip'] = 'no'

        return  d
    
    f = random.choice([rand_request, rand_response])
    jd = f()

    jdata = dict(jdata.items() + jd.items())
    return json.dumps(jdata)
    
def mock_logging_data_20003(ts, concurrency):
    jdata = {
        "staged_sig_names": random.choice(["", "XSS script tag end (Headers),XSS script tag (Headers)"]),
        "virus_name": random.choice(["N/A", "resident", "multipartite", "Directory", "Direct Action", "Macro", "FAT", "Network"]),
        "protocol": random.choice(['FTP', 'SMPTP', 'HTTP', 'DNS']),
        "sig_ids": "200001475,200000098,200001088",
        "sig_names": "XSS script tag end (Parameter) (2),XSS script tag (Parameter),alert() (Parameter)",
        "response": "Response logging disabled",
        "dest_port": "80",
        "sub_violations": "",
        "ip_with_route_domain": "10.250.64.100%0",
        "dest_ip": "10.250.17.%d" % random.choice([22, 104, 89]),
        "captcha_result": "not_received",
        "login_result": "N/A",
        "geo_location": "N/A",
        "username": "N/A",
        "mobile_application_version": "",
        "management_ip_address": "10.250.18.126",
        "mobile_application_name": "",
        "sig_set_names": "{Generic Detection Signatures},{Generic Detection Signatures},{Generic Detection Signatures}",
        "device_id": "N/A",
        "ip_addrewss_intelligence": "N/A",
        "request": "GET /DVWA/vulnerabilities/xss_r/?name=%3Cscript%3Ealert%28%22Your+system+is+infected%21+Call+999-888-7777+for+help.%22%29%3C%2Fscript%3E HTTP/1.1\\r\\nHost: 10.250.17.104\\r\\nConnection: keep-alive\\r\\nUpgrade-Insecure-Requests: 1\\r\\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36\\r\\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\\r\\nReferer: http://10.250.17.104/DVWA/vulnerabilities/xss_r/\\r\\nAccept-Encoding: gzip, deflate\\r\\nAccept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7\\r\\nCookie: security=low; PHPSESSID=l2h24don29mpl1650mp34hpbr3; TS01bd0d10=01428d52e7fe28902c791e7744e626939ac72a344fbc80b15aeba18eb65101c4107c48511e53b053e55cf61eb89752da9ecdd5019253cf128c8d0c0fc0955e5499ef16d454e62bc155dc062404d781c648dad1a041ddf57b6bfff4ac88d199cf2b415dcb1887be33e1c27c4baed0a9468992f943ad\\r\\n\\r\\n",
        "x_forwarded_for_header_value": "N/A",
        "route_domain": "0",
        "unit_hostname": "597200ed-322f-4001-baa2-55ab3c88942a.f5bigip.local",
        "blocking_exception_reason": "<131>Jul 16 03:41:32 597200ed-322f-4001-baa2-55ab3c88942a.f5bigip.local ASM:\"N/A\"",
        "policy_name": "/Common/DVWA-test",
        "type": "kafka",
        "staged_sig_set_names": "",
        "websocket_direction": "N/A",
        "websocket_message_type": "N/A",
        "policy_apply_date": "2020-07-15 09:45:09",
        "session_id": "9b5586855b961482",
        "method": "GET",
        "violations": "Attack signature detected",
        "http_class_name": "/Common/DVWA-test",
        "violation_rating": random.choice(['0', '0', '0', '0', '0', '0', '0', '1', '2', '3', '3', '4', '4', '4']),
        "uri": random.choice(["/DVWA/vulnerabilities/xss_r/", ]),
        "severity": random.choice(['Error', 'Warn', 'Debug']),
        "client_type": "Uncategorized",
        "attack_type": random.choice(["Cross Site Scripting (XSS)", "SQL-Injection", "CSRF"]),
        "ip_client": "10.250.64.%d" % random.randint(2, 255),
        "query_string": "name=%3Cscript%3Ealert%28%22Your+system+is+infected%21+Call+999-888-7777+for+help.%22%29%3C%2Fscript%3E",
        "staged_sig_ids": "",
        "suppoet_id": "2833372796841625208",
        "is_truncated": "",
        "date_time": "2020-07-16 03:41:32",
        "src_port": "54901",
        "request_status": random.choice(["blocked", "alarmed"]),
        "response_code": random.choice(["0", "200"])
    }

    return jdata