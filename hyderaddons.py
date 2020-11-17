import sys

from io import StringIO 
from abc import ABC, abstractmethod

logo = """\033[92m\t██░ ██▓██   ██▓▓█████▄ ▓█████  ██▀███  
\t▓██░ ██▒▒██  ██▒▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒
\t▒██▀▀██░ ▒██ ██░░██   █▌▒███   ▓██ ░▄█ ▒
\t░▓█ ░██  ░ ▐██▓░░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄  
\t░▓█▒░██▓ ░ ██▒▓░░▒████▓ ░▒████▒░██▓ ▒██▒
\t ▒ ░░▒░▒  ██▒▒▒  ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
\t ▒ ░▒░ ░▓██ ░▒░  ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░
\t ░  ░░ ░▒ ▒ ░░   ░ ░  ░    ░     ░░   ░ 
\t ░  ░  ░░ ░        ░       ░  ░   ░     
\t        ░ ░      ░                      
\t
\033[0m"""

class ModuleBaseClass(ABC):
    
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass
    
    @property
    @abstractmethod
    def safe(self):
        pass
    
    @abstractmethod
    def run(self, sshclient, args, server):
        pass


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def red(text):
        return '\033[91m' + str(text) + '\033[0m'

    @staticmethod
    def orange(text):
        return '\033[93m' + str(text) + '\033[0m'

    @staticmethod
    def blue(text):
        return '\033[94m' + str(text) + '\033[0m'

    @staticmethod
    def green(text):
        return '\033[92m' + str(text) + '\033[0m'

# Capturing class credits
# https://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

shared_pub_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDncs3ZXpt7FuaUY4FtWNSkBzuj8A/fzBQPCBaZk7mnF4p0i8BYorBPqGu3ltQK3vMrgV8w7A9PkVds56YPrLQuT8RJaMGOMgnGc4DacECz5Wg1yTFDZn+ZNkWsPlA3VRBzactFyjgxoxquw7gvVBq5h6OKvsQ4AVTUllLpWunC6D0swmFGi3NnitKBKiaqO7juv7oSdxMPtrJli+5aYd/gN44vm1yzPzxCOLeCcRJKW513mqVfYv6mwytdTnkLVTLTKgqXBiP2k8PFYw4wYp6XRHEbPDbUZDQElu/oaRRIAbwj5TJ0K2pdmK7RnLbJV8n/7YaEnwr7TCxd/tRD8PeZ2i562sZT/2G5tLTQh0Ze2SX3RMwAOtROdPEllbSqthZN1dNT62vj3BYFm14rBOh+xwtTdHh5luEDoaNn3SH1tOGTE4HFDrLTM7uWlSl/3KBCYfxRjDeLjAvykv5q+S/tpjzBauFhpBk3M9xldBnFPMQmtWmZ10dGM/I0NVZI/5c='
