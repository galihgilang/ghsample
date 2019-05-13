using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System;

using SimpleJSON;

using Url = System.String;
using ObjectId = System.String;
// KpiSet = List<Kpi>
using KpiSet = System.Collections.Generic.List<Kpi>;
// ObjectKpiData = Dictionary<String, List<KpiSet>>
using ObjectKpiData = System.Collections.Generic.Dictionary<System.String, System.Collections.Generic.List<System.Collections.Generic.List<Kpi>>>;
// KpiData = Dictionary<String, ObjectKpiData>
// C# SHARP IS MY BOY
using KpiData = System.Collections.Generic.Dictionary<System.String, System.Collections.Generic.Dictionary<System.String, System.Collections.Generic.List<System.Collections.Generic.List<Kpi>>>>;

public class KpiManager : MonoBehaviour {
	private static float ALPHA = 0.9f;

	public KpiData kpiData = new KpiData();
	public List<String> urls = new List<String>();
	private Dictionary<String, bool> requestInProgress = new Dictionary<String, bool>();

	public KpiSet getKpiSet(String url, ObjectId objectId, int kpiSetId) {
		if(kpiData.ContainsKey(url) && 
				kpiData[url].ContainsKey(objectId) && 
				kpiData[url][objectId].Count > kpiSetId) {
			return kpiData[url][objectId][kpiSetId];
		} else {
			// return empty list in case we are asked for data before we received the first rest reponse
			var dummySet = new KpiSet();
			Kpi dummy = new Kpi();
			dummy.name = "Missing";
			dummy.value = "???";
			dummy.cellX = 0;
			dummy.cellY = 0;
			dummy.color = new Color(1.0f, 0.0f, 0.0f);
			dummySet.Add(dummy);
			return dummySet;
		}
	}
	
	void Start () {
		
	}

	private void parseJson(String url, String jsonString) {
		var json = JSON.Parse(jsonString);
		kpiData[url] = new ObjectKpiData();
		foreach(var objectId in json.Keys) {
			var objectData = json[objectId];
			kpiData[url][objectId] = new List<KpiSet>();
			for(int set = 0; set < objectData["kpiSets"].Count; ++set) {
				var kpiSet = objectData["kpiSets"][set];
				kpiData[url][objectId].Add(new KpiSet());
				for(int i = 0; i < kpiSet["kpis"].Count; ++i) {
					var kpi = new Kpi();
					kpi.name = kpiSet["kpis"][i]["name"];
					kpi.value = kpiSet["kpis"][i]["value"];
					kpi.cellX = kpiSet["kpis"][i]["cellX"];
					kpi.cellY = kpiSet["kpis"][i]["cellY"];
					if(!ColorUtility.TryParseHtmlString(kpiSet["kpis"][i]["color"], out kpi.color)) {
						kpi.color = new Color(0.0f, 0.0f, 0.0f);
					}
					kpi.color.a = ALPHA;
					kpiData[url][objectId][set].Add(kpi);
				}
			}
		}
	}

	IEnumerator getKpiData(String url) {
		requestInProgress[url] = true;
		using (UnityWebRequest req = UnityWebRequest.Get(url)) {
			req.SetRequestHeader("Authorization", "Basic YWJ1amFidWphOmdpdXNtbmw=");
			yield return req.SendWebRequest();
			while(!req.isDone)
				yield return null;
			//byte[] result = req.downloadHandler.data;
			//string weatherJSON = System.Text.Encoding.Default.GetString(result);
			//WeatherInfo info = JsonUtility.FromJson<WeatherInfo>(weatherJSON);
			//onSuccess(info);
			if(req.isHttpError || req.isNetworkError || req.responseCode != 200) {
				Debug.Log(String.Format("HTTP error: {0} - {1}", req.responseCode, req.error));
			} else {
				parseJson(url, req.downloadHandler.text);
			}
			requestInProgress[url] = false;
		}
	}

	void Update() {
		foreach(var url in urls) {
			if(!requestInProgress.ContainsKey(url) || !requestInProgress[url]) {
				StartCoroutine("getKpiData", url);
			}
		}
	}
}
