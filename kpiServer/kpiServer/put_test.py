import requests

testKpi = {"name": "Test Kpi", "value": 0, "cellX": 0, "cellY": 0, "color": "#000000"}
requests.put("http://localhost:5000", json={"testMachine": {"kpiSets": [{"kpis": [testKpi]}]}})