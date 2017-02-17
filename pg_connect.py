#!/usr/bin/python

#
# Simple script to test Postresql database connectivity 
# 
# Written by Amine BEN ASKER, @asker_amine
#                         Github.com/yurilaaziz
# Zabbix Value mapping : 
#     Name : pg status
#           -1 = DOWN
#           -2 = Authentication Failed
#           -3 = Name Resolving Error
#           -4 = Timeout
#            0 = Error
#            1 = UP


import psycopg2
import argparse
parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('--action', help='action : uptime | version | startup :: if any : check connectivity')
parser.add_argument('--dbhost', required=True, help='database host')
parser.add_argument('--dbname', required=True, help='database name')
parser.add_argument('--dbuser', required=True, help='database user')
parser.add_argument('--dbpassword', required=True, help='database password')
parser.add_argument('--dbport', required=True, help='database port')
parser.add_argument('--timeout', default=5, help='connection timeout')

args = parser.parse_args()


ERR_CODES = {
    'Connection refused': -1,
    'password authentication failed':-2,
    'could not translate host name':-3,
    'timeout expired':-4,
    }

queries={
    "version" : "select version();",
    "startup" : "select pg_postmaster_start_time();",
    "uptime"  : """select date_trunc('second', current_timestamp - pg_postmaster_start_time()) as "postgresqluptime";"""
    }

try:
    conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}' port='{4}' connect_timeout='{5}'".format(args.dbname,args.dbuser,args.dbhost,args.dbpassword,args.dbport,args.timeout))
    status = 1
except Exception as e:
    status = 0
    for err, code in ERR_CODES.iteritems():
        if err in e.message:
            status = code


if args.action in queries:
    try : 
        cur = conn.cursor()
        cur.execute(queries[args.action])
        rows = cur.fetchall()
        value = rows[0][0]
    except Exception as e:
        value = ""
    print value
else:
    print status
