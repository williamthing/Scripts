#!/usr/bin/env python

import bigsuds
import time
import sys

from common.methods import set_progress
from networks.models import F5LoadBalancer
from utilities.models import ConnectionInfo


def delete_virtual_server(b, virtualname):
    path = '/Common/{}'.format(virtualname)
    if path in b.LocalLB.VirtualServer.get_list():
        b.LocalLB.VirtualServer.delete_virtual_server([virtualname])
        set_progress("Successfully deleted Virtual Server '{}'".format(virtualname))
    else:
        set_progress("Virtual Server '{}' not found".format(virtualname))


def delete_pool(b, pool_name):
    path = '/Common/{}'.format(pool_name)
    if path in b.LocalLB.Pool.get_list():
        b.LocalLB.Pool.delete_pool([pool_name])
        set_progress("Successfully deleted Pool '{}'".format(pool_name))
    else:
        set_progress("Pool '{}' not found.".format(pool_name))

def delete_nodes(b, pool_members):
    for member in pool_members:
        path = '/Common/{}'.format(member)
        if path in b.LocalLB.NodeAddressV2.get_list():
            b.LocalLB.NodeAddressV2.delete_node_address([member])
            set_progress("Successfully deleted Node '{}'".format(member))
        else:
            set_progress("Node '{}' not found".format(member))


def run(job, logger=None):
    # makes connection to F5 Big IP
    credential = ConnectionInfo.objects.filter(name='F5BIGIP')
    if not credential:
        return "", "", ""

    try:
        f5_conn = credential[0]
        b = bigsuds.BIGIP(
            hostname=f5_conn.ip,
            username=f5_conn.username,
            password=f5_conn.password,
            debug=True
        )
    except Exception, e:
        set_progress("Error in connecting to F5 BIG-IP")

    virtualname = 'CloudBoltF5'
    pool_name = 'CloudBolt_Rocks'
    pool_members = ['52.24.240.88', '54.191.113.54']

    # functional process to delete load balancer in F5
    delete_virtual_server(b, virtualname)
    delete_pool(b, pool_name)
    delete_nodes(b, pool_members)

    return "", "", ""
