#!/bin/env bash

#APPNAME="/pedro/desenvolvimento/workspaces/workspaces-doutorado/workspace-rv/rvsec/rv-android/out/cryptoapp.apk"
##TIMEOUT=120
#QTESTING_DIR="/pedro/desenvolvimento/workspaces/workspaces-doutorado/workspace-rv/rvsec/rv-android/tools/qtesting"

APPNAME=$1
QTESTING_DIR=$2

#echo $APPNAME
#echo $TIMEOUT
#echo $QTESTING_DIR

cp -f $APPNAME $QTESTING_DIR/apks/app.apk
docker run -v $QTESTING_DIR/apks:/qtesting/apks --net=host -i --rm phtcosta/qtesting:0.0.1
       #python src/main.py -r apks/conf.txt
