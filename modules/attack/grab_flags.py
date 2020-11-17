import logging
from datetime import datetime
from hyderaddons import bcolors, ModuleBaseClass

class GrabFlags(ModuleBaseClass):

    name = "htbbg_grab_flags"
    description = """HackTheBox Battlegrounds flag grabber.
Requires FLAGFILE=loot.txt to be provided using the -e/--env switch.
"""
    safe = False

    def run(self, sshclient, args, server):
        if not args.env.get("FLAGFILE", None):
            logging.error("grab_flags module requires -e FLAGFILE=output.txt")
            return False
        _, opt_flag, _ = sshclient.exec_command("cat /opt/flag.txt || echo flagnotfound")
        opt_flag = opt_flag.read().decode().strip()
        _, root_flag, _ = sshclient.exec_command("cat /root/flag.txt || echo flagnotfound")
        root_flag = root_flag.read().decode().strip()
        with open(args.env["FLAGFILE"], 'a') as f:
            f.write(f"{datetime.utcnow()},{server['IP']},{opt_flag},{root_flag}\n")
        print("Flags grabbed and appended to the " + bcolors.orange(args.env["FLAGFILE"]))
        return True
