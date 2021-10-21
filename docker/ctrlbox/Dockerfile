# build with
#   docker build . -t f5networks/ctrlbox:latest

FROM centos:7

RUN yum update -y
RUN yum install -y epel-release
RUN yum update -y

RUN yum install -y vim tree gcc curl jq crontabs goaccess net-tools bind-utils

RUN yum install -y python-pip
RUN pip install eventlet requests

WORKDIR /root

ENTRYPOINT while true; do sleep 1; done
