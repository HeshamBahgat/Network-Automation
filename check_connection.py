#!/usr/bin/env python3

import os
import getpass
from telnet_check import Telnet_Connection
from ssh_check import SSH_Connection
import re

username = input("Enter Username: ")
password = getpass.getpass()

# define the host type firstly to make them ready for globaly use between functions
ssh_host = ""
telnet_host = ""

# load the devise IPs
with open("Devices_IPs") as IPs:
    Devices_IPs = IPs.read().splitlines()

# check the devices reachabilty and retuen True or false
def try_ping(Device_IP):
    # will involk the shell and try to ping
    response = os.system("ping -c 3 " + Devices_IP)
    print(f"pinging{Devices_IP}")
    Device_Status = ""
    # and then check the response...
    if response == 0:
        Device_Status = True
        print(Devices_IP, " Is Up....")
    else:
        Device_Status = False
        print(Devices_IP, "IS Down!!!")
    return Device_Status

# check the privilige mode and make sure its always in Privileged mode
def check_Privilege(previous_text):
    a = re.search(r"(.+$)", previous_text)
    check_priv = a.group(1)
    print("privilge is being checked")
    if ">" in check_priv:
        print("User mode")
        tn.write(b"enable\n")
        tn.write(b"cisco\n")
    elif "#" in check_priv:
        print("Privileged mode")
        pass

# use ssh for connection then retrun True if succeeded
# also make ssh_host in global to use in different functions
def call_ssh(Devices_IP):
    global ssh_host
    print("trying to connect via SSH")
    ssh_host  = SSH_Connection(username , password, Devices_IP)
    #host = SSH_Connection(username, password, Devices_IP)
    privilige = ssh_host .connect()
    if privilige:
        check_Privilege(privilige)
        #host.Savingn_config(Devices_IP)
        return True
    else:
        return False

# use telent for connection then retrun True if succeeded
# also make telnet_host in global to use in different functions
def call_telnet(Devices_IP):
    global telnet_host
    print("trying to connect via Telnet")
    telnet_host = Telnet_Connection(username , password, Devices_IP)
    #host = Telnet_Connection(username, password, Devices_IP)
    previous_text, n = telnet_host.connect()
    if n > 0:
        check_Privilege(previous_text)
    else:
        return False

# if ssh connection failed will switch to telnet
def switching_protocols(Devices_IP):
    protocol = call_ssh(Devices_IP)
    if protocol:
        connectio_protocols = "SSH" # to differntiate the connection in commen functions
        print("ssh connection + privilige done")
        return connectio_protocols
    elif protocol == False:
        call_telnet(Devices_IP)
        connectio_protocols = "Telnet" # to differntiate the connection in commen functions
        print("telnet connection + privilige done")
        return connectio_protocols

# if the connection succeeded will check the protocol then will svae configuration files
def saving_files(connection_protocol, Devices_IP):

    if connection_protocol == "SSH":
        ssh_host.Savingn_config(Devices_IP)
    elif connection_protocol == "Telnet":
        telnet_host.Savingn_config(Devices_IP)

# this is the main fuction will start from here
for Devices_IP in Devices_IPs:
    answer = try_ping(Devices_IP)
    if answer:
        connection_protocol = switching_protocols(Devices_IP)
        saving_files(connection_protocol, Devices_IP)
        print(connection_protocol)
    else:
        print("Move to another device")