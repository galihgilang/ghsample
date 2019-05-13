using System;
using UnityEngine;

public class Kpi {
    public String name;
    public String value;
    public Color color;
    public int cellX;
    public int cellY;

    public String toString() {
        return String.Format("{0}: {1} at {2},{3}", name, value, cellX, cellY);
    }
}
