#!/bin/sh 
#Define your Dictionary List here
#DEFINE COMPANIES IN comp.in file

#exec 3>&1 4>&2
#trap 'exec 2>&4 1>&3' 0 1 2 3
#exec 1>${LOGFILE} 2>&1
#set -x 

v_activity=0
v_out_file=""

Log()
{
 echo "[${USER}][`date +%d-%m-%y--%T`] - ${*}" >> ${LOGFILE}
}


CheckEnvSet()
{
if [ -z "$PYTHON_PATH" ]
then
      echo "Setup PYTHON_PATH is EMPTY - set in env.set file" 
      exit
else
      echo  "\$PYTHON PATH is set - Continue "
fi

# SQL LIETE was not working when using relattive path  .Had to be in the directory where the file is 
if [ -z "$SQLLITE_PATH" ]
then
      echo "Setup PYTHON_PATH is EMPTY - set in env.set file"
      exit
else
      echo  "\$SQLITE_PATH is set - Continue "
fi


}

SetEnv()
{

DirList=`awk '{print $2}' env.set`
PYTHON_PATH=$(echo $DirList | cut -d " " -f 1)
SQLLITE_PATH=$(echo $DirList | cut -d " " -f 2)

}

Invoketicketgen()
{
v_n=$1
v_out_file=$2 
${PYTHON_PATH}python3 ticket_gen.py -o $v_n -f $v_out_file
if [ $? -eq 0 ]; then
    echo "JSON File created in the same directory . File name = $v_out_file "
else
    echo "ERROR - in creating JSON FILE "
    exit 
fi

}


InvokeReadjson()
{
v_in_file=$1 
${PYTHON_PATH}python3 ticket_read.py -f $v_in_file
if [ $? -eq 0 ]; then
    echo "Success read JSON FILE. The output file is wirtten in CSV format in the current directory - FILE NAME:  structured_data.csv"
else
    echo "ERROR - in reading  JSON FILE "
    exit
fi


}

SQLlite3import()
{

BASE_PATH="$(pwd)"
#echo -e ".mode csv TICKET \n.import ${BASE_PATH}/structured_data.csv TICKET" > env.sql 
#echo "$BASE_PATH "
cd ${SQLLITE_PATH} # Linked library error in my test server - Seems LDD is messed up. 
NEW_PATH="$(pwd)"
echo -e ".mode csv TICKET \n.import ${BASE_PATH}/structured_data.csv TICKET" > env.sql 
sqlite3 ticket_db  "CREATE TABLE IF NOT EXISTS  TICKET(performed_at   datetime,   ticket_id  INT ,   performer_id INT ,   shipmentdate TEXT,   status TEXT,   agent_id INT );"
sqlite3 -csv  ticket_db  '.read env.sql'
sqlite3 ticket_db -header -column "select ticket_id , 
      ( case status when 'Closed' THEN CAST((julianday((substr(performed_at, 7, 4) || '-' || substr(performed_at, 4, 2) || '-' || substr(performed_at, 1, 2) || ' ' ||substr(performed_at, 12 , 2) || ':' ||substr(performed_at, 15 , 2) || ':' ||substr(performed_at, 18 ,2))) 
- julianday ('now') ) * 24 * 60 AS INTEGER) ELSE 0 END ) AS time_till_closed, 
      ( case status when 'Open' THEN CAST((julianday((substr(performed_at, 7, 4) || '-' || substr(performed_at, 4, 2) || '-' || substr(performed_at, 1, 2) || ' ' ||substr(performed_at, 12 , 2) || ':' ||substr(performed_at, 15 , 2) || ':' ||substr(performed_at, 18 ,2))) 
- julianday ('now') ) * 24 * 60 AS INTEGER) ELSE 0 END ) AS time_spent_open ,
      ( case status when 'Resolved' THEN CAST((julianday((substr(performed_at, 7, 4) || '-' || substr(performed_at, 4, 2) || '-' || substr(performed_at, 1, 2) || ' ' ||substr(performed_at, 12 , 2) || ':' ||substr(performed_at, 15 , 2) || ':' ||substr(performed_at, 18 ,2))) 
- julianday ('now') ) * 24 * 60 AS INTEGER) ELSE 0 END ) AS time_till_resolution,
      ( case status when 'Waiting for Customer' THEN CAST((julianday((substr(performed_at, 7, 4) || '-' || substr(performed_at, 4, 2) || '-' || substr(performed_at, 1, 2) || ' ' ||substr(performed_at, 12 , 2) || ':' ||substr(performed_at, 15 , 2) || ':' ||substr(performed_at, 18 ,2))) 
- julianday ('now') ) * 24 * 60 AS INTEGER) ELSE 0 END ) AS time_spent_waiting_on_customer,
      ( case status when 'Waiting for Third Party' THEN CAST((julianday((substr(performed_at, 7, 4) || '-' || substr(performed_at, 4, 2) || '-' || substr(performed_at, 1, 2) || ' ' ||substr(performed_at, 12 , 2) || ':' ||substr(performed_at, 15 , 2) || ':' ||substr(performed_at, 18 ,2))) 
- julianday ('now') ) * 24 * 60 AS INTEGER) ELSE 0 END ) AS time_spent_waiting_on_party,
      ( case status when 'Pending' THEN CAST((julianday((substr(performed_at, 7, 4) || '-' || substr(performed_at, 4, 2) || '-' || substr(performed_at, 1, 2) || ' ' ||substr(performed_at, 12 , 2) || ':' ||substr(performed_at, 15 , 2) || ':' ||substr(performed_at, 18 ,2))) 
- julianday ('now') ) * 24 * 60 AS INTEGER) ELSE 0 END ) AS time_till_pending
FROM 
TICKET ;"

}


function usage() {

        echo
        echo "Usage: $0 [ -o ]  [ -f <filename> ]"
        echo
        echo " -o                -- Number of activities in the jSON file "
        echo " -f                -- Export JSON File name "

}




#MAIN 
#Invoketicketgen
while getopts o:f:h? x
do
   case "$x" in
        o)        v_activity=$OPTARG;;
        f)        v_out_file=$OPTARG;;


        h|H|?|*) usage && exit
        esac

done

SetEnv
CheckEnvSet

Invoketicketgen ${v_activity} ${v_out_file}
InvokeReadjson ${v_out_file}
SQLlite3import 
