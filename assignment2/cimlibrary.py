import requests
from requests.exceptions import HTTPError
import xml.etree.ElementTree as ET
import pywbem

class CIMHandler:
    # Set config parameters

    def __init__(self):
        self.root_url = "http://ttm4128.item.ntnu.no:5988/cimom"

    def send_req(self, className):

        classname = className
        namespace = 'root/cimv2'

        conn = pywbem.WBEMConnection(self.root_url, ('user','password'),
                default_namespace=namespace,
                no_verification=True)
        try:
            insts = conn.EnumerateInstances(classname)
        except pywbem.Error as exc:
            print('Operation failed: %s' % exc)
        else:
            print('Retrieved %s instances' % (len(insts)))
            payload = "path= "
            for inst in insts:
                payload+=str(inst.path) + '\n'
                payload += str(inst.tomof()) + '\n'

            return payload
