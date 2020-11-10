# Hyder

```
██░ ██▓██   ██▓▓█████▄ ▓█████  ██▀███  
▓██░ ██▒▒██  ██▒▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒
▒██▀▀██░ ▒██ ██░░██   █▌▒███   ▓██ ░▄█ ▒
░▓█ ░██  ░ ▐██▓░░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄  
░▓█▒░██▓ ░ ██▒▓░░▒████▓ ░▒████▒░██▓ ▒██▒
 ▒ ░░▒░▒  ██▒▒▒  ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
 ▒ ░▒░ ░▓██ ░▒░  ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░
 ░  ░░ ░▒ ▒ ░░   ░ ░  ░    ░     ░░   ░ 
 ░  ░  ░░ ░        ░       ░  ░   ░     
        ░ ░      ░                      

```

Hyder is a project which aims to automate some actions which one can do during HackTheBox Battlegrounds game. Depending on the modules, this tool can be used elsewhere as well and fit perfectly.

Hyder name can be interpreted in two ways. First, it's "hi there" written short. Second, it's "hide" but cooler. That's why there are two main functionalities in this project: `attack` and `defend` modules.

## Screenshots

Hyder can give you dense output:

![https://imgur.com/W5RqmJh.png](https://imgur.com/W5RqmJh.png)

..or can provide output of each module per each server it executes command on:

![https://imgur.com/ARKGnTr.png](https://imgur.com/ARKGnTr.png)

..or list available modules for given modules category:

![https://imgur.com/GTIVXDi.png](https://imgur.com/GTIVXDi.png)


## Installation



## Usage

Hyder is built using argparse so you can provide `-h/--help` anywhere, anytime.

### Main help

```
$ ./hyder.py -h

usage: hyder.py [-h] {attack,defend,list} ...

Battlegrounds multitool

positional arguments:
  {attack,defend,list}

optional arguments:
  -h, --help            show this help message and exit
```

### Module help

```
$ ./hyder.py attack -h

usage: hyder.py attack [-h] [-v] [-s] [-e ENV] [-t TIMEOUT] [--sshkey SSHKEY] [-H HOSTS] [-i IP] [-u USER] [-p PWD] [--backdoor_pwd BACKDOOR_PWD] modules

positional arguments:
  modules               Which modules to run, can include asterisk to wildcard or use 'all' to run all of them. For instance: 'backdoor*'. To list attack modules execute: hyder.py attack list attack

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose
  -s, --safe            Run only 'safe' modules
  -e ENV, --env ENV     Pass variable to the module. This can be used many times. For instance: -e HOST=10.10.10.10 -e PORT=4444
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout for the SSH connect. Defaults to: 3
  --sshkey SSHKEY       RSA key to be used in SSH connection. Point to a file location and use 'sshkey' as password in config file
  --backdoor_pwd BACKDOOR_PWD
                        Defaults to: Passw0rd

targets:
  -H HOSTS, --hosts HOSTS
                        File to read hosts from in the form of 'IP:user:pass' per line. Excludes usage of -i/-u/-p
  -i IP, --ip IP        Server IP to connect. Excludes usage of -H
  -u USER, --user USER  Username to use for the connection. Excludes usage of -H
  -p PWD, --pwd PWD     Password to use for the connection. Excludes usage of -H
```

### Example usage

```
# Lists available attack modules
./hyder.py list attack

# Assumes a hosts file which has entries in the form of IP:username:password per line
# Increases verbosity
./hyder.py attack all -H hosts -v

# When you only want to provide credentials for one server
./hyder.py attack all -i 172.17.0.2 -u root -p Passw0rd

# When you only want to provide credentials for one server
# When you only want backdoor modules
./hyder.py attack all -i 172.17.0.2 -u root -p Passw0rd

# When you only want to provide credentials for one server
# When you only want backdoor modules
# When you only want "safe" modules
./hyder.py attack backdoor* --ip 172.17.0.2 --user root --pwd Passw0rd --safe
```
