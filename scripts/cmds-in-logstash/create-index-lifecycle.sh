#!/bin/bash

host_endpoint="http://elasticsearch:9200"

index_lifecyle_home=/usr/share/logstash/index-lifecycle

timeout=150

echo "Waiting for es to be ready"
echo -n "Waiting for es to be ready ..."
wait=0
while true; do 
    if [ $wait -ge $timeout ]; then 
        echo "timeout for waiting for es readiness."
        exit 1
    fi
    res_code=`curl $host_endpoint -s -o /dev/null -w "%{http_code}"`
    if [ "$res_code" = "200" ]; then 
        echo " OK"
        break; 
    else 
        echo -n "."
    fi

    wait=$(($wait + 1))
    sleep 1
done

echo -n "Setting read_only_allow_delete to false ... "
curl -X PUT -s -w "%{http_code}" -H "Content-Type: application/json" $host_endpoint/_settings \
  -d '{ "index": { "blocks": { "read_only_allow_delete": "false" } } }'
echo

(
  cd $index_lifecyle_home
  for n in `ls`; do 
    response=`curl -s -o /dev/null $host_endpoint/_ilm/policy/$n -w "%{http_code}"`
    if [ "$response" != "200" ]; then
      echo -n "Creating index_lifecyle: $n ... "
      curl -X PUT -s -w "%{http_code}" \
        -H "Content-Type: application/json" \
        $host_endpoint/_ilm/policy/$n -d@$n
      echo
    fi
  done
)
