import datetime
import os
import sys

from flask import jsonify, request, Response

from kpiServer import app
from .util import eprint

MACHINE_KPI_TIMEOUT = datetime.timedelta(seconds=5)

USERNAME_ENV = "KPI_SERVER_USERNAME"
PASSWORD_ENV = "KPI_SERVER_PASSWORD"
if not (USERNAME_ENV in os.environ and PASSWORD_ENV in os.environ):
    eprint("Please set environment variables for HTTP basic auth: {} and {}".format(USERNAME_ENV, PASSWORD_ENV))
    sys.exit(1)

# This will map machine names to kpi generator addresses
# We use this to detect if multiple generators try to send data for the same machine
remoteAddrMachineAssocMap = {}
kpiData = {}
lastMachineUpdate = {}

def getRequesterIp():
    # If behind a proxy, such as Nginx, the public IP is included in the header
    if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
        request.environ["REMOTE_ADDR"]
    else:
        request.environ["HTTP_X_FORWARDED_FOR"]

def checkAuth():
    auth = request.authorization
    return auth and auth.username == os.environ[USERNAME_ENV] and auth.password == os.environ[PASSWORD_ENV]

# http://flask.pocoo.org/snippets/8/
def authorize():
    return Response("Could not verify your access level for that URL.\n"
    "You have to login with proper credentials", 401,
    {"WWW-Authenticate": "Basic realm=\"Login Required\""})

def removeTimedout(kpiData):
    now = datetime.datetime.now()
    timedout = [machine for machine in kpiData.keys() if now >= lastMachineUpdate[machine] + MACHINE_KPI_TIMEOUT]
    for machine in timedout:
        kpiData.pop(machine)

def saveJsonData(kpiData, jsonData):
    requesterIp = getRequesterIp()
    ok = True
    for machineName in jsonData:
        if not machineName in remoteAddrMachineAssocMap:
            remoteAddrMachineAssocMap[machineName] = requesterIp

        if remoteAddrMachineAssocMap[machineName] == requesterIp: # owned, may overwrite
            kpiData[machineName] = jsonData[machineName]
            lastMachineUpdate[machineName] = datetime.datetime.now()
        else: # modify unowned machine kpis
            eprint("{} attempts to modify kpi data of machine {}, previously owned by {}".format(
                requesterIp, machineName, remoteAddrMachineAssocMap[machineName]))
            ok = False 
    return ok

@app.route("/", methods=["GET", "PUT"])
def data():
    if request.method == "GET":
        if checkAuth():
            removeTimedout(kpiData)
            return jsonify(kpiData)
        else:
            eprint("Failed Authentication")
            return authorize()
    elif request.method == "PUT":
        jsonData = request.get_json()
        if jsonData == None:
            eprint("Malformed PUT request (no JSON data) from {}".format(getRequesterIp()))
            return "Malformed PUT request (no JSON data)", 400 # Bad Request
        else:
            if saveJsonData(kpiData, jsonData):
                return "", 200
            else:
                return "Attempt to modify kpi data of a machine not owned", 403 # Forbidden