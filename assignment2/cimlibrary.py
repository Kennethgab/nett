import requests
from requests.exceptions import HTTPError


class CIMHandler(self):
    # Set config parameters
    self.root_url = "http://ttm4128.item.ntnu.no:5988/cimom"
    self.protocol_version = "CIMProtocolVersion=2.0"
    self.CIMOperation = "MethodCall"



    def __init__(self):
        pass


    # Send request to CIM 
    def send_req(self,className):
        pass

