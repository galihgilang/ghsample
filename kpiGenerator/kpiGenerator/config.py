import os

import psutil

from .util import Kpi, threshColor

KPI_SERVER_ENDPOINT = "http://magicleap.sudohack.net"

defaultThreshColor = threshColor("#00aa00", (50, "#aaaa00"), (80, "#aa0000"))

def cpuUsage():
    return int(psutil.cpu_percent())

def memUsage():
    return int(psutil.virtual_memory().percent)

machineName = None
# Please make sure that all Kpi objects have a update interval > 0, so the main loop gets some sleep
kpis = [
    Kpi("Username", lambda: os.environ["USERNAME"], 0, 0, "#000000", None),
    Kpi("CPU Load", cpuUsage, 1, 0, defaultThreshColor, 2.0),
    Kpi("Memory Usage", memUsage, 2, 0, defaultThreshColor, 2.0),
]