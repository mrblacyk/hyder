import sys
sys.path.append('../..')

modules = []

# Register modules here

# Deploy Snoopy
from .deploy_snoopy import DeploySnoopy
modules.append(DeploySnoopy)

# Local TCPDump
from .local_tcpdump import LocalTcpdump
modules.append(LocalTcpdump)
