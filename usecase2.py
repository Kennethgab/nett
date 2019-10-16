import subprocess
from enum import Enum
import re
import datetime
import os.path
import smtplib
from tabulate import tabulate
import time


def send_email(user, to, body, pwd):
    to = to
    user = user
    pwd = pwd
    smtpserver = smtplib.SMTP("smtp.office365.com", 587)

    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(user, pwd)

    header = 'To:' + to + '\n' + 'From: ' + user + '\n' + \
        'Subject:group 4 monitor report {} \n'.format(datetime.datetime.now())
    msg = header + '\n\n'
    msg += body
    smtpserver.sendmail(user, to, msg)
    print('done!')
    smtpserver.close()


def construct_body(nodes):
    msg = ''
    for name, values in nodes.items():
        ip = values[0]
        msg += "Node:" + name + " TTL: " + values[1]
        msg += '\n'
        table = nodes[name][3:]
        msg += tabulate(table, headers=[
            "Time", "Ipv4 Datagrams", "Difference"])
        msg += '\n'
    return msg


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


def main():
    username = input("Type in your email: ")
    password = input("Email password for SMTP: ")
    to = input("Email recipient: ")

    # sahara lab pc -> [IP, TTL,  [time,packets,diff]*]
    computers = {'sahara17': ['129.241.209.17'],
                 'sahara18': ['129.241.209.18']}
    com = 'ttm4128'

    # ipSystemStatsHCInReceives.ipv4 = .1.3.6.1.2.1.4.31.1.1.19.ipv4 number of ipv4 packets
    datagramsoid = ".1.3.6.1.2.1.4.31.1.1.4.1"
    sysnameoid = " 1.3.6.1.2.1.1.5.0"
    ttloid = "ipDefaultTTL.0"

    # get initial read for pkt diff
    for name, values in computers.items():
        ip = values[0]
        print("Polling computer {}, with IP {} at time {}".format(
            name, ip, datetime.datetime.now()))
        sysname = os_callout('snmpget', com, ip,
                             sysnameoid)
        ipv4_datagrams = os_callout(
            "snmpget", com, ip, datagramsoid)
        row = [datetime.datetime.now(), ipv4_datagrams, 0]
        ttl = os_callout(
            "snmpget", com, ip, ttloid)
        computers[name].append(ttl)
        computers[name].append(row)

    time.sleep(60)
    tablelength = 0
# loop every minute, send mail and wipe buffer every 5th minute.
    while True:
        for name, values in computers.items():
            ip = values[0]
            print("Polling computer {}, with IP {} at time {}".format(
                name, ip, datetime.datetime.now()))
            sysname = os_callout('snmpget', com, ip,
                                 sysnameoid)
            ipv4_datagrams = os_callout(
                "snmpget", com, ip, datagramsoid)

            prev_pkt_count = computers[name][-1][1]
            row = [datetime.datetime.now(), ipv4_datagrams, int(
                ipv4_datagrams) - int(prev_pkt_count)]
            computers[name].append(row)
            table = computers[name][3:]
            tablelength = len(table)
            print(tabulate(table, headers=[
                "Time", "Ipv4 Datagrams", "Difference"]))

        if tablelength == 5:
            tablelength = 0
            body = construct_body(computers)
            print("body of email: ")
            print(body)
            send_email(username, to, body, password)

            computers = {'sahara17': ['129.241.209.17'],
                         'sahara18': ['129.241.209.18']}

        time.sleep(60)


if __name__ == "__main__":
    main()
