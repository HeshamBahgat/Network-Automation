import random, sys, os

from colorama import init, deinit, Fore, Style


class Validate_IP():
    def __init__(self):
        pass

    def host_ip(self, ip_address):
        print("\n")
        # Checking IP address validity
        #Checking octets
        ip = ip_address.split(".")
        if (len(ip) == 4) and \
            (1 <= int(ip[0]) <= 223) and \
            (int(ip[0]) != 127) and \
            (int(ip[0]) != 169 or int(ip[1]) != 254) and \
            (0 <= int(ip[1]) <= 255 and 0 <= int(ip[2]) <= 255 and 0 <= int(ip[3]) <= 255):
            print(ip_address, "is valid")
            return True
        else:
            return False

    def host_mask(self, mask):
        masks = [255, 254, 252, 248, 240, 224, 192, 128, 0]
        #Checking Subnet Mask Validity
        #Checking octets
        mask = subnet_mask.split(".")
        if len(mask) == 4:
            if (int(mask[-4]) in masks and int(mask[-4]) !=0) and mask[-3] == "0" and mask[-2] == "0" and mask[-1] == "0":
                return True

            elif (int(mask[0]) == 255) and (int(mask[1]) in masks) and mask[2] == "0" and mask[3] == "0":
                return True

            elif (int(mask[0]) == 255) and (int(mask[1]) == 255) and int(mask[2]) in masks and mask[3] == "0":
                return True

            elif (int(mask[0]) == 255) and (int(mask[1]) == 255) and (int(mask[2]) == 255) and int(mask[3]) in masks:
                return True
            else:
                return False
        else:
            return False

    def ping(self, Device_IP):
        # check the devices reachabilty and retuen True or false
        # will involk the shell and try to ping
        response = os.system("ping -c 3 " + Device_IP)
        print(f"pinging{Device_IP}")
        Device_Status = ""
        # and then check the response...
        if response == 0:
            Device_Status = True
            print(Device_IP, " Is Up....")
        else:
            Device_Status = False
            print(Device_IP, "IS Down!!!")
        return Device_Status