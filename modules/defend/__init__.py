import sys

sys.path.append('../..')

modules = []

# Register modules here

# Backdoor Users
from .deploy_snoopy import DeploySnoopy
modules.append(DeploySnoopy)
