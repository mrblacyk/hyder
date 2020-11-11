import logging
from hyderaddons import bcolors

class DeploySnoopy:
    
    name = "deploy_snoopy"
    description = """Install snoopy.
Provide -e SNOOPYRESTART=yes to restart apache2 and smbd services afterwards"""
    safe = True

    def run(self, sshclient, args, server):
        # Remove leftovers
        sshclient.exec_command("rm -rf /usr/local/lib/libsnoopy.so")
        sshclient.exec_command("rm -rf /etc/snoopy.ini")

        sftp = sshclient.open_sftp()
        sftp.put("./modules/defend/files/libsnoopy.so.2.4.8", "/usr/local/lib/libsnoopy.so")
        sftp.put("./modules/defend/files/snoopy.ini", "/etc/snoopy.ini")
        sftp.close()

        print((
            "Uploaded two files: "
            f'{bcolors.orange("/usr/local/lib/libsnoopy.so")}, '
            f'{bcolors.orange("/etc/snoopy.ini")}'
        ))

        sshclient.exec_command((
            "touch /etc/ld.so.preload &&"
            "grep '/usr/local/lib/libsnoopy.so' /etc/ld.so.preload ||"
            "echo '/usr/local/lib/libsnoopy.so' >> /etc/ld.so.preload;"
        ))

        if args.env.get("SNOOPYRESTART"):
            logging.info("Restarting apache2 and smbd services")
            sshclient.exec_command((
                "systemctl restart apache2 &>/dev/null;"
                "systemctl restart smbd &>/dev/null;"
            ))
            print("Restarted " + bcolors.orange("apache2,smbd") + " services")
        return True
