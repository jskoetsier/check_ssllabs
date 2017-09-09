#!/usr/bin/env python3
#
#
# This is the API hook, which is ran independly from jenkins.
#
# Revision 09-09-2017 - 16:04
#
# Copyright 2017 - Sebastiaan Koetsier <s.koetsier@amsio.com>
#

import sys
import argparse
import os
import requests
import time
import logging
import json
import pickle

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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', action='store', help="Hostname to scan", dest="host", required='true')
    args = parser.parse_args()
    host = (args.host)

    if args.host == '':
        print ('No valid hostname given')
        sys.exit(1)
    if args.host != '':
        if os.path.isfile("/var/spool/ssllabs/"+host+".dat"):
            os.remove("/var/spool/ssllabs/"+host+".dat")
            repose=newScan(host)
            pickle.dump(response, open("/var/spool/ssllabs/"+host+".dat", "wb"))
            sys.exit(0)
        else:
            response=newScan(host)
            pickle.dump(response, open("/var/spool/ssllabs/"+host+".dat", "wb"))
            sys.exit(0)
    else:
        print ('Please use -H to add hostname')
        sys.exit(1)

if __name__ == "__main__":
    main()



