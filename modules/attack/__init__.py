import sys
sys.path.append('../..')

modules = []

# Register modules here

# Backdoor Users Ssh Dir
from .backdoor_users_ssh_dir import BackdoorUsersSshDir
modules.append(BackdoorUsersSshDir)

# Backdoor Nologin False
from .backdoor_nologin_false import BackdoorNologinFalse
modules.append(BackdoorNologinFalse)

# Backdoor Passwd
from .backdoor_passwd import BackdoorPasswd
modules.append(BackdoorPasswd)

# HTB Battlegrounds flag grabber
from .htbbg_grab_flags import GrabFlags
modules.append(GrabFlags)
