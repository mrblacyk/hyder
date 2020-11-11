import logging

class LocalTcpdump:

    name = "local_tcpdump_systemd"
    description = """Run tcpdump listening on any interface using systemd. Writes output to /root/.dump.pcap by default
Provide -e LTCPD_FILE=/root/.dump2.pcap to control output file
Privide -e LTCPD_INT=ens33 to control monitored interface
"""
    safe = True

    def run(self, sshclient, args, server):
        out_file = args.env.get("LTCPD_FILE", "/root/dump.pcap")
        interface = args.env.get("LTCPD_INT", "any")
        tcpdump_systemd_service = """[Unit]
Description=Local TCPDump service

[Service]
Type=simple
ExecStart=/bin/bash /usr/bin/.local_tcpdump.sh

[Install]
WantedBy=multi-user.target
"""
        tcpdump_shell_file = f"""#!/bin/bash

nohup tcpdump -nni {interface} -s 0 -w {out_file}
"""
        sshclient.exec_command("pkill tcpdump &>/dev/null")

        _, stdout, _ = sshclient.exec_command((
            f"echo '''{tcpdump_systemd_service}''' > /etc/systemd/system/localtcpd.service &&"
            f"echo '''{tcpdump_shell_file}''' > /usr/bin/.local_tcpdump.sh &&"
            "chmod 644 /etc/systemd/system/localtcpd.service &&"
            "chmod +x /usr/bin/.local_tcpdump.sh &&"
            "systemctl daemon-reload &&"
            "systemctl start localtcpd &&"
            f"echo OK"
        ))

        stdout = stdout.read().decode().strip()
        if "OK" in stdout:
            return True
        return False
