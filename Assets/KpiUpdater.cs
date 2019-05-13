using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;

using CellIndex = System.Int32;
// KpiMap = Dictionary<CellIndex, Dictionary<CellIndex, GameObject>>
using KpiMap = System.Collections.Generic.Dictionary<System.Int32, System.Collections.Generic.Dictionary<System.Int32, UnityEngine.GameObject>>;

public class KpiUpdater : MonoBehaviour {
	private const float CELL_SIZE = 0.15f;
	private const float CELL_PADDING = 0.035f;

	public String url;
	public String objectId;
	public int kpiSetId;
	public GameObject kpiPrefab;

	public int cellsX;
	public int cellsY;

	private GameObject kpiManager;
	private KpiMap kpiMap = new KpiMap();

	// Use this for initialization
	void Start () {
		kpiManager = GameObject.Find("KpiManager");
	}

	String formatKpi(Kpi kpi) {
		return String.Format("{0}:\n{1}", kpi.name, kpi.value);
	}

	void createKpiGameObject(Kpi kpi) {
		if(!kpiMap.ContainsKey(kpi.cellY)) kpiMap[kpi.cellY] = new Dictionary<CellIndex, GameObject>();
		var kpiGameObject = Instantiate(kpiPrefab);
		kpiGameObject.GetComponent<RectTransform>().SetParent(gameObject.transform);
		float kpiSetWidth = cellsX * CELL_SIZE + (cellsX - 1) * CELL_PADDING;
		float kpiSetHeight = cellsY * CELL_SIZE + (cellsY - 1) * CELL_PADDING;
		var pos = new Vector3(-kpiSetWidth/2 + kpi.cellX * (CELL_SIZE + CELL_PADDING),
							  kpiSetHeight/2 - kpi.cellY * (CELL_SIZE + CELL_PADDING),
							  0.0f);
		kpiGameObject.GetComponent<RectTransform>().localPosition = pos;
		kpiGameObject.GetComponent<RectTransform>().localRotation = Quaternion.identity;

		kpiMap[kpi.cellY][kpi.cellX] = kpiGameObject;
	}
	
	// Update is called once per frame
	void Update () {
		// turn off all kpis
		foreach(Transform childTrafo in gameObject.transform) {
			GameObject child = childTrafo.gameObject;
			child.SetActive(false);
		}

		var kpis = kpiManager.GetComponent<KpiManager>().getKpiSet(url, objectId, kpiSetId);
		foreach(var kpi in kpis) {
			if(kpiMap.ContainsKey(kpi.cellY) && kpiMap[kpi.cellY].ContainsKey(kpi.cellX)) {
				// entity exists => update it
				GameObject obj = kpiMap[kpi.cellY][kpi.cellX];
				obj.SetActive(true);
				obj.transform.GetChild(0).gameObject.GetComponent<Image>().color = kpi.color;
				obj.transform.GetChild(1).gameObject.GetComponent<Text>().text = formatKpi(kpi);
			} else {
				createKpiGameObject(kpi);
			}
		}
	}
}
