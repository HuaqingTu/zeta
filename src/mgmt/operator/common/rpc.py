# SPDX-License-Identifier: MIT
# Copyright (c) 2020 The Authors.

# Authors: Sherif Abdelwahab <@zasherif>
#          Phu Tran          <@phudtran>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:The above copyright
# notice and this permission notice shall be included in all copies or
# substantial portions of the Software.THE SOFTWARE IS PROVIDED "AS IS",
# WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
# THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import logging
import json
from common.common import run_cmd

logger = logging.getLogger()


class TrnRpc:
    def __init__(self, ip, mac, itf='eth0', benchmark=False):
        self.ip = ip
        self.mac = mac
        self.phy_itf = itf

        # transitd cli commands
        self.trn_cli = f'''/trn_bin/transit -s {self.ip} '''
        self.trn_cli_load_transit_xdp = f'''{self.trn_cli} load-transit-xdp -i {self.phy_itf} -j'''
        self.trn_cli_unload_transit_xdp = f'''{self.trn_cli} unload-transit-xdp -i {self.phy_itf} -j'''
        self.trn_cli_update_ep = f'''{self.trn_cli} update-ep -i {self.phy_itf} -j'''
        self.trn_cli_get_ep = f'''{self.trn_cli} get-ep -i {self.phy_itf} -j'''
        self.trn_cli_delete_ep = f'''{self.trn_cli} delete-ep -i {self.phy_itf} -j'''
        self.trn_cli_load_pipeline_stage = f'''{self.trn_cli} load-pipeline-stage -i {self.phy_itf} -j'''
        self.trn_cli_unload_pipeline_stage = f'''{self.trn_cli} unload-pipeline-stage -i {self.phy_itf} -j'''

        if benchmark:
            self.xdp_path = "/trn_xdp/trn_transit_xdp_ebpf.o"
        else:
            self.xdp_path = "/trn_xdp/trn_transit_xdp_ebpf_debug.o"

    def get_substrate_ep_json(self, ip, mac):
        jsonconf = {
            "tunnel_id": "0",
            "ip": ip,
            "eptype": "0",
            "mac": mac,
            "veth": "",
            "remote_ips": [""],
            "hosted_iface": ""
        }
        jsonconf = json.dumps(jsonconf)
        return jsonconf

    def update_substrate_ep(self, ip, mac):
        jsonconf = self.get_substrate_ep_json(ip, mac)
        cmd = f'''{self.trn_cli_update_ep} \'{jsonconf}\''''
        logger.info("update_substrate_ep: {}".format(cmd))
        returncode, text = run_cmd(cmd)
        logger.info("returns {} {}".format(returncode, text))

    def update_ep(self, ep):
        peer = ""
        droplet_ip = ep.get_droplet_ip()
        # Only detail veth info if the droplet is also a host
        if (droplet_ip and self.ip == droplet_ip):
            peer = ep.get_veth_peer()

        jsonconf = {
            "tunnel_id": ep.get_tunnel_id(),
            "ip": ep.get_ip(),
            "eptype": ep.get_eptype(),
            "mac": ep.get_mac(),
            "veth": ep.get_veth_name(),
            "remote_ips": ep.get_remote_ips(),
            "hosted_iface": peer
        }

        jsonconf = json.dumps(jsonconf)
        cmd = f'''{self.trn_cli_update_ep} \'{jsonconf}\''''
        logger.info("update_ep: {}".format(cmd))
        returncode, text = run_cmd(cmd)
        logger.info("returns {} {}".format(returncode, text))

    def delete_substrate_ep(self, ip):
        jsonconf = {
            "tunnel_id": "0",
            "ip": ip,
        }
        jsonconf = json.dumps(jsonconf)
        cmd = f'''{self.trn_cli_delete_ep} \'{jsonconf}\''''
        logger.info("delete_substrate_ep: {}".format(cmd))
        returncode, text = run_cmd(cmd)
        logger.info(
            "delete_substrate_ep returns {} {}".format(returncode, text))

    def delete_ep(self, ep):
        jsonconf = {
            "tunnel_id": ep.get_tunnel_id(),
            "ip": ep.get_ip(),
        }
        jsonconf = json.dumps(jsonconf)
        cmd = f'''{self.trn_cli_delete_ep} \'{jsonconf}\''''
        log_string = "delete_ep for a {} {}".format(ep.type, ep.ip)
        logger.info(log_string)
        returncode, text = run_cmd(cmd)
        logger.info("returns {} {}".format(returncode, text))
