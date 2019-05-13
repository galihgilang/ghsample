import datetime

def threshColor(defaultColor, *args):
    lastThresh = None
    for arg in args:
        thresh, color = arg
        assert(lastThresh == None or thresh > lastThresh)
        lastThresh = thresh

    def colorFunc(value):
        for arg in reversed(args):
            thresh, color = arg
            if value >= thresh:
                return color 
        return defaultColor

    return colorFunc

# I don't like about this:
# * both self.updateInterval and self.nextUpdate contain information about updates should happen at all
# * some values can be fixed values or callback (e.g. color) and I think the interface is not clean
class Kpi(object):
    # updateInterval = None => never updates
    # color can be a callable that takes the value as a parameter
    def __init__(self, name, valueFunc, cellX, cellY, color, updateInterval):
        self.name = name 
        assert(callable(valueFunc))
        self.valueFunc = valueFunc
        self.value = self.valueFunc()
        self.cellX = cellX
        self.cellY = cellY
        self.color = color 
        self.updateInterval = updateInterval
        self.nextUpdate = None if updateInterval == None else datetime.datetime.now()

    def updateValue(self):
        now = datetime.datetime.now()
        if self.updateInterval != None and self.nextUpdate <= now:
            self.nextUpdate = now + datetime.timedelta(seconds=self.updateInterval)
            valueFunc = self.valueFunc
            self.value = valueFunc()

    # Make sure the value has been updated before this is called!
    def getColor(self):
        if callable(self.color):
            colorFunc = self.color
            return colorFunc(self.value)
        else:
            assert(isinstance(self.color, str))
            return self.color

    def getObject(self):
        self.updateValue()
        return {
            "name": self.name,
            "value": self.value,
            "cellX": self.cellX,
            "cellY": self.cellY,
            "color": self.getColor(),
        }

if __name__ == "__main__":
    defaultThreshColor = threshColor("#00aa00", (50, "#aaaa00"), (80, "#aa0000"))
    for i in range(0, 100, 10):
        print(i, defaultThreshColor(i))
