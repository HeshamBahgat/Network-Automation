import paramiko, socket, time, datetime
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoAuthenticationException, AuthenticationException, NetMikoTimeoutException
from paramiko.ssh_exception import SSHException, NoValidConnectionsError

from colorama import init, deinit, Fore, Style


class SSH_Connection():
    def __init__(self, user, psw, Host):
        self.user = user
        self.psw = psw
        self.Host = Host

    def try_login(self):
        print("Connecting to device' " + self.Host)
        ip_address_of_device = self.Host
        ios_device = {
            "device_type": "cisco_ios",
            "ip": ip_address_of_device,
            "username": self.user,
            "password": self.psw
        }
        try:
            self.net_connect = ConnectHandler(**ios_device)
            self.Telnet_privi = True
            print("connection is okay")

        except NoValidConnectionsError:
            self.Telnet_privi = False
            print("Unable to connect to port 22 either no route to the host or not configured")
        except NetMikoTimeoutException:
            self.Telnet_privi = False
            print("Time out")
        except (AuthenticationException):
            self.Telnet_privi = False
            print ("Authentication failure: ")
        except (NetMikoAuthenticationException):
            self.Telnet_privi = False
            print("Timeout to device: ")
        except (EOFError):
            self.Telnet_privi = False
            print("End of file while attempting device ")
        except (SSHException):
            self.Telnet_privi = False
            print("End Issue. Are you sure SSH is enabled?")
        except Exception as unknown_error:
            self.Telnet_privi = False
            print (" Some other error: %d" %(unknown_error))
        except (socket.error, socket.gaierror):
            self.Telnet_privi = False
            print("socket error")
        except(EOFError or SSHException):
            self.Telnet_privi = False
            print("lets see")
        return self.Telnet_privi

    def connect(self):
        self.try_login()
        if self.Telnet_privi:
            # will get the prompt so can extract either hostname or to know the privilage level
            self.prompt = self.net_connect.find_prompt()
            return self.prompt
        else:
            return self.Telnet_privi

    def Savingn_config(self, device_ipaddr):
        self.net_connect.send_command("terminal length 0")
        config_data = self.net_connect.send_command("show run")

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

        config_filename = (f"SSH:{st}:config-" + device_ipaddr)  # Important - create unique configuration
        print("---- Writing Configuration: ", config_filename)
        with open(config_filename, "w") as config_out: config_out.write(config_data)