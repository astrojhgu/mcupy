#!/bin/sh

echo "-L/usr/lib -lboost_python`python -V 2>/dev/stdout|awk '{print $2}'|grep ^3 >/dev/null && echo 3`"
