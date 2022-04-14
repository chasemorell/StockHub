!/bin/bash

brew install coreutils
brew install postgresql

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

if [[ -n `psql -lqt | cut -d \| -f 1 | grep -w "$dbname"` ]]; then
    dropdb $dbname
fi
createdb $dbname


psql -af create.sql $dbname
cd $datadir

read -p "Do you want to run getStockData.py to load stocks from csv (Y/N) ?" y
if [ $y == "Y" ] ; then
   python3 $mybase/getStockData.py a $mybase
fi

psql -af $mybase/load.sql $dbname
