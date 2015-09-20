#!/usr/bin/env python

import bigsuds
import time
import sys

from common.methods import set_progress

def create_pool(b, pool, lbmethod, pl_mems):
    pool = '/Common/%s' % pool
    pmlist = []
    for x in pl_mems:
        pm = {}
        for key in x:
            y = []
            y.append(key)
            y.append(x[key])
            pm['address'] = str(y[0])
            pm['port'] = int(y[1])
            pmlist.append(pm)
    try:
        pllist = b.LocalLB.Pool.get_list()
        if pool in pllist:
            b.LocalLB.Pool.add_member_v2([pool], [pmlist])
        else:
            b.LocalLB.Pool.create_v2([pool],[lbmethod],[pmlist])

        return b.LocalLB.Pool.get_member_v2([pool])
        set_progress("Successfully created pool '{}'".format(pool))
    except Exception, e:
        set_progress("Error in creating pool")


def create_virtual_server(b, virtualname, address, port, member_pool):
    try:
        b.LocalLB.VirtualServer.create(
            definitions = [{'name': [virtualname],'address': [address], 'port': [port], 'protocol': 'PROTOCOL_TCP'}],
            wildmasks = ['255.255.255.255'], resources = [{'type': 'RESOURCE_TYPE_POOL', 'default_pool_name': [member_pool]}],
            profiles = [[{'profile_context': 'PROFILE_CONTEXT_TYPE_ALL', 'profile_name': 'tcp'}]]
        )
        set_progress("Successfully created virtual server '{}'".format(virtualname))
    except:
        set_progress("Error in creating virtual server")


def run(job, logger=None):
    # makes connection to F5 Big IP
    try:
        b = bigsuds.BIGIP(
            hostname = '10.60.103.79', username='admin', password='cloudbolt', debug=True
        )
    except Exception, e:
        set_progress("Error in connecting to F5 BIG-IP")

    # Naming of Pool
    pool_name = 'CloudBolt_Rocks'
    #pool_name = 'CloudBolt' + str(int(time.time()))
    lb_meth = 'LB_METHOD_ROUND_ROBIN'
    # Taking in pool members aka Instance Ip's from job
    servers = job.parent_job.server_set.all()
    server_ips = []
    # Takes in port
    #server_port = int({{ port }})
    server_port = 80
    for server in servers:
        server_ips.append({str(server.ip): server_port})
        set_progress("Adding instance ip {} to pool".format(server.ip))

    poolinfo = create_pool(b, pool_name, lb_meth, server_ips)
    for x in poolinfo:
        set_progress("Pool: {}".format(pool_name))
        for y in x:
            set_progress("\t%s:%d" % (y['address'], y['port']))

    # created pool and pool members, create VS and add default pool
    virtualname = 'CloudBoltF5'
    address = '10.60.60.88'
    create_virtual_server(b, virtualname, address, server_port, pool_name)

    return "", "", ""
