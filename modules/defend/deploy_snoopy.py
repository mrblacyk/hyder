import logging

class DeploySnoopy:
    
    name = "deploy_snoopy"
    description = ""

    def run(self, sshclient, args, server):
        logging.info("I'm running! " + self.name)
        return True
