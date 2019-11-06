import requests
from requests.exceptions import HTTPError
import xml.etree.ElementTree as ET

class CIMHandler:
    # Set config parameters

    def __init__(self):
        self.root_url = "http://ttm4128.item.ntnu.no:5988/cimom"

    # Send request to CIM
    def send_req(self,className):
        tree = ET.parse("cimtemplate.xml")
        tree = tree.getroot()
        xml_str = ET.tostring(tree).decode()
        headers = {'CIMProtocolVersion': '2.0', 'CIMOperation' : 'MethodCall', 'Content-Type' : 'application/xml'}
        r = requests.post(self.root_url, data=xml_str, headers=headers)
        print(r.content)


    def write_xml(self, className):
        pass

def main():
    cim = CIMHandler()
    cim.send_req("CIM_OperatingSystem")

if __name__ == "__main__":
    main()
