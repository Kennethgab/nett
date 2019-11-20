import subprocess


class SNMPHandler:
    snmpGet = 'snmpget'
    snmpGetNext = 'snmpgetnext'
    snmpBulkGet = 'snmpbulkget'
    snmpWalk = 'snmpwalk'
    snmpTable = 'snmptable'
    operations = [snmpBulkGet,snmpwalk, snmpGet, snmpGetNext, snmpTable]
    
    def __init__(self,comstring, ip):
        self.ip = ip
        self.comstring = comstring


    
    def send_req(self, operation, oid) 
        
        operation = operation.lower()

        try:
            if operation in operations:
                return self._os_callout(operation, oid)
        except:
            pass


        



    def _os_callout(self, operation, oid):
         snmpcmd = "{} -v 2c -c {} {} {}".format(
        operation, self.comstring, self.ip, oid)
        p = subprocess.Popen(snmpcmd, stdout=subprocess.PIPE, shell=True)
        output = p.communicate()[0]
    return output


