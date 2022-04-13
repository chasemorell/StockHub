#!/bin/bash

#brew install coreutils
#brew install postgresql

mypath=`realpath $0`
mybase=`dirname $mypath`
cd $mybase

datadir="${1:-data/}"
if [ ! -d $datadir ] ; then
    echo "$datadir does not exist under $mybase"
    exit 1
fi

source ../.flaskenv
dbname=$DB_NAME
psql -af createStockRelations.sql $dbname
cd $datadir
