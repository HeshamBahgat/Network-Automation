import telnetlib
import os
import time, datetime

class Telnet_Connection:
    def __init__(self, user, psw, Host):
        self.user = user
        self.psw = psw
        self.Host = Host
    def try_to_connect(self):
        # will telnet to the host
        try:
            print(f"telneting to {self.Host}")
            self.tn = telnetlib.Telnet(self.Host, timeout=20)
            self.Telnet_privi = True
        except ConnectionRefusedError:
            self.Telnet_privi = False
            print("telnet not configured")
        except OSError:
            self.Telnet_privi = False
            print('No route to host')

    def try_login(self):
        # will login and return login invalid if thereis a problem
        self.tn.read_until(b"Username: ")
        self.tn.write(self.user.encode('ascii') + b"\n")
        if self.psw:
            self.tn.read_until(b"Password: ")
            self.tn.write(self.psw.encode('ascii') + b"\n")
            time.sleep(1)
        # expect will use regular expression to match the ouput after login
        # n == 0 means match happened
        # match the string that need to match
        # previous_text all the output in the shell either login successed ofr faild
        n, match, self.previous_text = self.tn.expect([br"% Login invalid", br"\#"], 10)
        self.decode_text = (self.previous_text.decode("ascii"))
        if n == 0:
            print("Username and Password failed - giving up")
        else:
            pass
        return self.decode_text, n

    def connect(self):
        Privilege = ""
        self.try_to_connect()
        if self.Telnet_privi:
            Privilege = self.try_login()
        return Privilege

    def Savingn_config(self, device_ipaddr):
        self.tn.write(b"terminal length 0\n")
        self.tn.write(b"show run\n")
        self.tn.write(b"exit\n")

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        config_filename = (f"Telnet:{st}:config-" + device_ipaddr)  # Important - create unique configuration


        readoutput = self.tn.read_all()
        print("---- Writing Configuration: ", config_filename)
        with open(config_filename, "w") as config_out: config_out.write(readoutput.decode('ascii'))