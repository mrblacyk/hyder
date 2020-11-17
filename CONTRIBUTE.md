# How to contribute

You want to contribute a module or two? Awesome! There are basically two steps:

1) You have to write a module ;-) Chose a category (attack/defend) and create a file under it. To keep it consitent, please name the file the same name you will use in class variable `name`.
2) Register your module in `__init__.py` file of a given category (attack/defend)  

## Module structure

Each module has to be contained in a single class containing four major components:

* A class which derives from ModuleBaseClass (abstract class to check everything was implemented)
* Three **class** variables:
    - `name` (a str variable),
    - `description` (a str variable),
    - `safe` (a bool variable).
* One **instance** method named `run` taking four arguments:
    - `self`,
    - `sshclient`,
    - `args`,
    - `server`.
* `run` method must return `True` indicating it was executed correctly. Everything else will be treated as a fail.

### `sshclient`

`sshclient` is just `paramiko.client.SSHClient` object. It should be already connected to a given server. You can refer to [paramiko documentation](http://docs.paramiko.org/en/stable/api/client.html) for further help. Paramiko for Dummies 101 when writing a module:

```python
# To execute command
sshclient.exec_command("whoami")

# To upload a file
## Open SFTP channel
sftp = sshclient.open_sftp()

## The first argument is local location, the second one is remote location
sftp.put("./modules/defend/files/libsnoopy.so.2.4.8", "/usr/local/lib/libsnoopy.so")

## Close unused channel
sftp.close()
```

### `args`

Basically it's [argparse Namespace object](https://docs.python.org/3/library/argparse.html#argparse.Namespace). You can access here arguments provided to launch hyder with. Main usage predicted for module creators is to access `args.env` which is a dictionary containing all key and values provided with `-e` argument.

```python
# Hyder launched like so
# ./hyder.py attack all -H hosts -e LHOST=127.0.0.1 -e LPORT=4444
#
# This is how you can access those LHOST and LPORT vars in two ways
# 1) Better way because you will get None if the key was not provided
args.env.get("LHOST")

# 2) If key does not exist, this will trigger exception
# You have to handle the exception. This way is not recommended
args.env["LHOST"]
```
### `server`

This is dictionary file containing keys `IP`, `user` and `password`. You have there information about currently server on which module runs.

## Registering the module

It's easy as adding two lines of code and one comment. Here's the `__init__.py` file from `defend` directory:

```python
import sys
sys.path.append('../..')

modules = []

# Register modules here

# Deploy Snoopy
from .deploy_snoopy import DeploySnoopy
modules.append(DeploySnoopy)

# (..)

# Your Module       <---------------------------
from .yourmodule import YourModule  # assumes your module file name is yourmodule.py
modules.append(YourModule)
```

# Example

Module:

```python
import logging, datetime
from hyderaddons import ModuleBaseClass

class PrintTime(ModuleBaseClass):
    name = "printtime"
    description = "Module which prints time so operator know when hyder was run when viewing console history of any sort"
    safe = True

    def run(self, sshclient, args, server):
        logging.debug(datetime.datetime.utcnow())
        logging.debug("Server IP: " + server.get("IP", "Unknown"))
        print(f"{server.get('IP')}: {datetime.datetime.utcnow()}")

        return True

```

Defend `__init__.py` file:

```python
import sys
sys.path.append('../..')

modules = []

# Register modules here
(..)

# Print Time
from .printtime.py import PrintTime
modules.append(PrintTime)
```

# Note

Hyder is built in a way that by default it prints only module's `print()` from the first server. For the rest of servers, a simple `OK` or `FAILED` is displayed (don't forget to return `True` when everything was executed properly). Operator can change this behavior by providing `-v` when executing hyder. `logging` however is printed indepdently so it's crucial you use `logging.error("Error message")` and `logging.warning("Warning message")` when you can catch in the module something going sideways.
