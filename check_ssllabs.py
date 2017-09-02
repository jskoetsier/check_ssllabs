#!/usr/bin/env python3
#
#
# Copyright 2017 - Sebastiaan Koetsier
#
#
import sys
import argparse
import os
import requests
import time
import logging
import json

API = 'https://api.ssllabs.com/api/v2/'

def requestAPI(path, payload={}):

    url = API + path

    try:
        response = requests.get(url, params=payload)
    except requests.exception.RequestException:
        logging.exception('Request failed.')
        sys.exit(1)

    data = response.json()
    result = data
    return data


def resultsFromCache(host, publish='off', startNew='off', fromCache='on', all='done'):
    path = 'analyze'
    payload = {
                'host': host,
                'publish': publish,
                'startNew': startNew,
                'fromCache': fromCache,
                'all': all
              }
    data = requestAPI(path, payload)
    return data


def newScan(host, publish='off', startNew='on', ignoreMismatch='on', endpoints='gradeTrustIgnored'):
    path = 'analyze'
    payload = {
                'host': host,
                'publish': publish,
                'startNew': startNew,
                'ignoreMismatch': ignoreMismatch,
                'endpoints': all

              }
    results = requestAPI(path, payload)

    payload.pop('startNew')

    while results['status'] != 'READY' and results['status'] != 'ERROR':
        time.sleep(30)
        results = requestAPI(path, payload)
    return results

def statusresults(grade):
    ExitOK=1
    ExitWarn=2
    ExitCrit=3
    ExitUnknown=4

    if grade == "A":
        print ('OK - Grade is:', grade)
        sys.exit(ExitOK)
    elif grade == "A+":
        print ('OK - Grade is:', grade)
        sys.exit(ExitOK)
    elif grade == 'A-':
        print ('OK - Grade is:', grade)
        sys.exit(ExitOK)
    elif grade == 'B':
        print ('WARN - Grade is:', grade)
        sys.exit(ExitWarn)
    elif grade == 'C':
        print ('WARN - Grade is:', grade)
        sys.exit(ExitWarn)
    else:
        print ('UNKNOWN - Grade is:', grade)
        sys.exit(ExitUnknown)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', action='store', help="Hostname to scan", dest="host", required='true')
    args = parser.parse_args()
    host = (args.host)

    if args.host == '':
        print ('No valid hostname given')
        sys.exit(1)
    if args.host != '':
        response=newScan(host)
        grade=response['endpoints'][0]['gradeTrustIgnored']
        statusresults(grade)
    else:
        print ('Please use -H to add hostname')
        sys.exit(2)



if __name__ == "__main__":
    main()



