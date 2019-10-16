import subprocess
import re
import datetime
from tabulate import tabulate
import time


def snmpformat(cmd, text):
    # filters to only data requested based on cmd used

    regs = {
        'snmpget': '= \w+: (.+)'
    }

    m = re.search(regs[cmd], text.decode("utf-8"))
    if m:
        return m.group(1)


def os_callout(cmd, com, ip, oid):

    snmpcmd = "{} -v 2c -c {} {} {}".format(
        cmd, com, ip, oid)
    p = subprocess.Popen(snmpcmd, stdout=subprocess.PIPE, shell=True)
    output = p.communicate()[0]
    output = snmpformat(cmd, output)
    return output


def send_trap(ip, com, latest_measure, difference):

    cmd = "snmptrap"
    # text to set trap value
    tid = " '' NTNU-NOTIFICATION-MIB::trapExample SNMPv2-MIB::sysLocation.0 s 'just here in sahara, chilling.'"
    os_callout(cmd, com, ip, oid)


def main():

    datagramsoid = ".1.3.6.1.2.1.4.31.1.1.4.1"
    sysnameoid = " 1.3.6.1.2.1.1.5.0"
    ttloid = "ipDefaultTTL.0"

    ip = "129.241.209.18"
    com = "ttm4128"
    threshold = 1300
    measures = []
    first_measure = os_callout("snmpget", com, ip, datagramsoid)
    measures.append(int(first_measure))
    while True:
        time.sleep(120)
        new_measure = os_callout("snmpget", com, ip, datagramsoid)
        measures.append(int(new_measure))
        print("Taken new measure: " + new_measure)
        difference = measures[-1] - measures[-2]
        if(difference >= threshold):
            print("Sending a trap!")
            send_trap(ip, com, measures[-1], difference)


if __name__ == "__main__":
    main()
