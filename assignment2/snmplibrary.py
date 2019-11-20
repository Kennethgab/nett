import subprocess
import re


class SNMPHandler:
    
    def __init__(self,comstring, ip):
        self.ip = ip
        self.comstring = comstring


   
   
    def send_req(self, operation, oid):
        snmpGet = 'snmpget'
        snmpGetNext = 'snmpgetnext'
        snmpBulkGet = 'snmpbulkget'
        snmpWalk = 'snmpwalk'
        snmpTable = 'snmptable'
        operations = [snmpBulkGet,snmpWalk, snmpGet, snmpGetNext, snmpTable]
     
        operation = operation.lower()

        if operation in operations:
            return self._os_callout(operation, oid)


        



    def _os_callout(self, operation, oid):
        snmpcmd = "{} -v 2c -c {} {} {}".format(
        operation, self.comstring, self.ip, oid)
        print(snmpcmd)
        p = subprocess.Popen(snmpcmd, stdout=subprocess.PIPE, shell=True)
        output = p.communicate()[0]
        regs = '= \w+: (.+)'
        text = re.search(regs, output.decode('utf-8'))
        return output


if __name__ == '__main__':
    snmp = SNMPHandler('ttm4128', '129.241.209.4')
    data = snmp.send_req('snmpget', 'system.sysDescr.0')
    print(data)




