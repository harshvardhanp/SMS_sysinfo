#!/usr/bin/python3

from twilio.rest import Client
import sys
import platform
import time


account = "XXXXXXXXXXXXXXXXXXXXXXXXXX"
token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
twilio_cell = 'XXXXXXXXXXXXXXX'
my_cell = 'XXXXXXXXXXXX'

client = Client(account, token)


def main():
    if sys.platform == 'win32':
        msg = getwin_msg()
        print(msg)
    else:
        msg = getlinux_msg()
        print(msg)

    message = client.messages.create(to=my_cell, from_=twilio_cell, body=msg)


def getwin_msg():

    import wmi
    import datetime
    w = wmi.WMI()
    sysinfo = w.Win32_ComputerSystem()[0]
    host_name = sysinfo.DNSHostName
    os_name = platform.platform()
    sys_type = platform.machine()

    msg = "Computer Name:{}\nOS Name:{}\nSystem type:{}\n".format(host_name, os_name, sys_type)
    msg += "Time:{}".format(time.strftime("%c"))

    for interface in w.Win32_NetworkAdapterConfiguration(IPEnabled=1):
        v = ''
        v += v + str(interface.Description) + str(interface.MACAddress)
        for ip_address in interface.IPAddress:
            v += str(ip_address)
        # print(v)
        msg += v
    # print(msg)

    return msg


def getlinux_msg():

    import netifaces as ni
    os_name = platform.platform()
    sys_type = platform.machine()

    msg = "OS Name:{}\nSystem type:{}\n".format(os_name, sys_type)

    v = ''
    for i in ni.interfaces():
        ni.ifaddresses(i)
        v += ni.ifaddresses(i)[ni.AF_INET][0]['addr'] + "\t"
        v += ni.ifaddresses(i)[ni.AF_LINK][0]['addr'] + "\n"

    v += "Time:{}".format(time.strftime("%c"))
    msg += v
    return msg


if __name__ == '__main__':
    main()
