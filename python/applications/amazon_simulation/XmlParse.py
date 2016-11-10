import xml.sax

class NodeHandle(xml.sax.ContentHandler):
    def __init__(self):
        self.id = ""
        self.lon = ""
        self.lat = ""

    def startElement(self, name, attrs):
        self.CurrentData = name
        if name == "node":
            print "*****Node*****"
            id = attrs["id"]
            self.id = id
            print "id", self.id
            lon = attrs["lon"]
            self.lon = lon
            print "lon", self.lon
            lat = attrs["lat"]
            self.lat = lat
            print "lat", self.lat

if (__name__ == "__main__"):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = NodeHandle()
    parser.setContentHandler(Handler)
    parser.parse("RoadsMeters.osm.xml")