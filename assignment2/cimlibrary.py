import requests
from requests.exceptions import HTTPError
import xml.etree.ElementTree as ET
import pywbem
from pywbem import CIMInstanceName
import shlex

class CIMHandler:
    # Set config parameters

    def __init__(self):
        self.root_url = "http://ttm4128.item.ntnu.no:5988/"

    
    def send_req(self, operation, className=None, instanceName=None):
        '''
        operations (str) allowed: enumerateInstances, enumerateInstanceNames, getInstance,
                            enumerateClassNames, enumerateClasses, getClass

        getInstance needs instanceName and className defined
        enumerateInstances, enumerateInstanceNames and getClass needs className defined
        enumerateClassNames and enumerateClass needs neither className nor instanceName
        '''
        payload = ''
        classname = className
        instancename = instanceName
        namespace = 'root/cimv2'

        conn = pywbem.WBEMConnection(self.root_url, ('user','password'),
                default_namespace=namespace,
                no_verification=True)
       
        try:
            if operation == "enumerateInstances":
                insts = conn.EnumerateInstances(classname)
                print('Retrieved %s instances' % (len(insts)))
                payload = "path= "
                for inst in insts:
                    payload += str(inst.path) + '\n'
                    payload += str(inst.tomof()) + '\n'

            if operation == "enumerateInstanceNames":
                insts = conn.EnumerateInstanceNames(classname)
                print('Retrieved %s instances' % (len(insts)))
                payload = ""
                for inst in insts:
                    payload += str(inst) + '\n'

            if operation == "getInstance":
                instance_paths = conn.EnumerateInstanceNames(classname)
                instancepath = None
                for path in instance_paths:
                    if str(path.get("Name")) == instancename:
                        instancepath = path
                if not instancepath:
                    raise RuntimeError("Found no instancename for that class")
                instance = conn.GetInstance(instancepath)
                payload = f"Instance {instancename} in class {classname}:\n"
                for keyitem in instance.items():
                    payload += f"{keyitem[0]}: {keyitem[1]}\n"

            if operation == "enumerateClasses":
                classes = conn.EnumerateClasses(DeepInheritance=True)
                payload = "Classes:\n"
                for classinfo in classes:
                    payload += f"{classinfo.classname}:\n"
                    for key in classinfo.properties:
                        payload += f"{key}\n"
                    payload += '\n'

            if operation == "enumerateClassNames":
                classes = conn.EnumerateClassNames(DeepInheritance=True)
                print('Retrieved %s classes' % (len(classes)))
                payload = "Classes:\n"
                for classinfo in classes:
                    payload += str(classinfo) + '\n'

            if operation == "getClass":
                classinfo = conn.GetClass(classname)
                payload = f"{classname}:\n"
                for key in classinfo.properties:
                    payload += f"{key}\n"
            return payload
        except pywbem.Error as exc:
            print('Operation failed: %s' % exc)
            return str(exc)


if __name__ == "__main__":
    cimConn = CIMHandler()
   


