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
import pickle
from pprint import pprint

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

def results(host):
    results=pickle.load(open("/var/spool/ssllabs/"+host+".dat", "rb"))
    grade=results['endpoints'][0]['gradeTrustIgnored']
    statusresults(grade)
    sys.exit

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', action='store', help="Results", dest="host", required='true')
    args = parser.parse_args()
    host = (args.host)

    if args.host == '':
        print ('No valid hostname given')
        sys.exit(1)
    if args.host != '':
        if os.path.isfile("/var/spool/ssllabs/"+host+".dat"):
            results(host)
        else:
            print ("UNKNOWN - Domain not in jenkins job, please add.")
            sys.exit(4)
    else:
        print ('Please use -H to add hostname')
        sys.exit(2)



if __name__ == "__main__":
    main()



