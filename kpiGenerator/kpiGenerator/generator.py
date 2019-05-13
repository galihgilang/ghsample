import datetime
import socket
import sys
import time 

import requests

from . import config

def getNextUpdate():
    return min(kpi.nextUpdate for kpi in config.kpis if kpi.nextUpdate != None)

def sleepUntil(until):
    delta = (until - datetime.datetime.now()).total_seconds()
    if delta > 0:
        time.sleep(delta)

def main():
    while True:
        kpiObjects = []
        for kpi in config.kpis:
            kpiObjects.append(kpi.getObject())

        machineName = config.machineName or socket.gethostname()
        fullObject = {machineName: {"kpiSets": [{"kpis": kpiObjects}]}}
        
        #print("POST", fullObject)
        try:
            req = requests.put(config.KPI_SERVER_ENDPOINT, json=fullObject, timeout=1)
            if req.status_code != 200:
                print("Error PUTing data to KPI server: HTTP {} - {}".format(req.status_code, req.text), file=sys.stderr)
        except requests.exceptions.ConnectTimeout as e:
            print("Request timed out.", file=sys.stderr)
        
        sleepUntil(getNextUpdate())

if __name__ == "__main__":
    main()
