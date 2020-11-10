#!/usr/bin/env python3 

import paramiko
import argparse
import os
import logging
import crypt
import socket
import modules
import hyderaddons

from re import search as re_search

global servers
servers = []
global connections
connections = []


if os.environ.get("LOGLEVEL"):
    logging.basicConfig(level=os.environ.get("LOGLEVEL"))
else:
    logging.basicConfig(level=logging.WARNING)
logging.getLogger("paramiko").setLevel(logging.WARNING)


def initialize_connections(args):
    global connections
    global servers
    for server in servers:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
        if server["pwd"] == "sshkey" and args.sshkey:
            try:
                client.connect(
                    server["IP"], username=server["user"],
                    key_filename=args.sshkey, timeout=args.timeout
                )
            except (paramiko.ssh_exception.NoValidConnectionsError, socket.timeout):
                logging.error("Could not connect to %s@%s" % (server["user"], server["IP"]))
                continue
        else:
            if server["pwd"] == "sshkey" and not args.sshkey:
                logging.warning("sshkey defined as password but ssh key not provided!")
            try:
                client.connect(
                    server["IP"], username=server["user"],
                    password=server["pwd"], timeout=args.timeout
                )
            except (paramiko.ssh_exception.NoValidConnectionsError, socket.timeout):
                logging.error("Could not connect to %s@%s" % (server["user"], server["IP"]))
                continue
        logging.debug("Unsetting HISTORY env in the ssh connection (" + server["IP"] + ")")
        client.exec_command("unset HISTORY")
        connections.append([server, client])

def loop_through_servers(func, args):
    global connections
    outputs = []
    for server, client in connections:
        logging.debug(client)
        logging.debug(server)
        with hyderaddons.Capturing() as output:
            cmd_output = func(client, args, server)
        outputs.append([server["IP"], cmd_output, output.copy()])
        del output
    if not args.verbose:
        for output in outputs:
            if output[1] == True:
                print("\n".join(output[2]))
                break
    print("")
    print("Module executions: ")
    for output in outputs:
        if output[1] == True:
            print("\t -> " + hyderaddons.bcolors.green(output[0]) + ": OK")
        else:
            print("\t -> " + hyderaddons.bcolors.red(output[0]) + ": FAILED")
            logging.info(output[2])
        if args.verbose:
            print("\n".join(["\t" + x for x in output[2]]))
            print("\n")


def close_connections():
    global connections
    for _, client in connections:
        client.close()
    print("")

def execute_modules(args):
    initialize_connections(args)

    if args.modules == 'all':
        logging.debug("Executing all modules")
        for module in modules.__getattribute__(args.which).modules:
            print(hyderaddons.bcolors.blue("\n" + "#" * 80))
            print(
                hyderaddons.bcolors.blue("\t->") + " MODULE:    " + module.name
            )
            print(hyderaddons.bcolors.blue("#" * 80))
            loop_through_servers(module().run, args)

    else:
        logging.debug("I'm feeling picky with modules: " + args.modules)
        didrun = False
        for module in modules.__getattribute__(args.which).modules:
            if re_search("^" + args.modules.replace('*', '.+') + "$", module.name):
                print(hyderaddons.bcolors.blue("\n" + "#" * 80))
                print(
                    hyderaddons.bcolors.blue("\t->") + " MODULE:    " + module.name
                )
                print(hyderaddons.bcolors.blue("#" * 80))
                loop_through_servers(module().run, args)
                didrun = True
        if not didrun:
            logging.warning("No module ran")
    
    close_connections()

def list_modules(args):
    try:
        modules_list = modules.__getattribute__(args.category).modules
    except AttributeError:
        return logging.error("Category not found")
    print("Available modules: ")
    for module in modules_list:
        print("\t- " + module.name)
    return True

def common_parser_args(parser):
    parser.add_argument("modules", type=str, help="Which modules to run, can include asterisk to wildcard or use 'all' to run all of them. For instance: 'backdoor*'. To list attack modules execute: " + parser.prog + " list attack")
    parser.add_argument("-v", "--verbose", required=False, action="store_true")
    parser.add_argument("-s", "--safe", required=False, action="store_true", help="Run only 'safe' modules")
    parser.add_argument("-t", "--timeout", required=False, type=int, help="Timeout for the SSH connect. Defaults to: 3", default=3)
    parser.add_argument(
        "--sshkey", required=False,
        help="RSA key to be used in SSH connection. Point to a file location and use 'sshkey' as password in config file"
    )
    group = parser.add_argument_group('targets')
    group.add_argument(
        "-H", "--hosts", required=False, type=str,
        help="File to read hosts from in the form of 'IP:user:pass' per line. Excludes usage of -i/-u/-p"
    )
    group.add_argument("-i", "--ip", required=False, type=str, help="Server IP to connect. Excludes usage of -H")
    group.add_argument("-u", "--user", required=False, type=str, help="Username to use for the connection. Excludes usage of -H")
    group.add_argument("-p", "--pwd", required=False, type=str, help="Password to use for the connection. Excludes usage of -H")

def args_okay(args):
    if args.__getattribute__('hosts'):
        if args.__getattribute__('ip') or args.__getattribute__('user') or args.__getattribute__('pwd'):
            return False
        return True
    elif args.__getattribute__('ip') and args.__getattribute__('user') and args.__getattribute__('pwd'):
        if args.__getattribute__('hosts'):
            return False
        return True
    else:
        logging.error("Provide -H/--hosts OR -i/--ip AND -u/--user AND -p/--pwd")
        return False

def main():
    # Set up argparse
    parser = argparse.ArgumentParser(description="Battlegrounds multitool")
    parser.set_defaults(which='main')
    subparsers = parser.add_subparsers()

    attack_parser = subparsers.add_parser("attack")
    attack_parser.set_defaults(which='attack')

    defend_parser = subparsers.add_parser("defend")
    defend_parser.set_defaults(which='defend')

    common_parser_args(attack_parser)
    common_parser_args(defend_parser)

    list_parser = subparsers.add_parser("list")
    list_parser.set_defaults(which='list')
    choices = subparsers.choices.keys()
    choices = [x for x in choices if x != 'list']
    list_parser.add_argument("category", help="Available categories to list modules are: " + str(choices))

    attack_parser.add_argument("--backdoor_pwd", required=False, type=str, default="Passw0rd", help="Defaults to: Passw0rd")
    args = parser.parse_args()

    if args.which == 'main':
        return parser.print_help()
    elif args.which == 'list':
        return list_modules(args)

    if not args_okay(args):
        return logging.error("Not enough arguments")

    global servers
    if args.hosts:
        with open(args.hosts, "r") as f:
            for line in f:
                line = line.strip().split(":")
                # Expected format: IP:user:password
                servers.append({
                    "IP": line[0].strip(), "user": line[1].strip(), "pwd": line[2].strip()
                })
    else:
        servers.append({
            "IP": args.ip.strip(), "user": args.user.strip(), "pwd": args.pwd.strip()
        })
    
    if 'which' in args:
        if 'modules' in args:
            return execute_modules(args)
        else:
            return subparsers.choices[args.which].print_help()
    else:
        logging.debug("Reached the end of the main function")
        return parser.print_help()

if __name__ == "__main__":
    print(hyderaddons.logo)
    main()
