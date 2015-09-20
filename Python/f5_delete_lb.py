#!/usr/bin/env python

import bigsuds
import time
import sys

#from common.methods import set_progress


def delete_virtual_server(b, virtualname):
    path = '/Common/{}'.format(virtualname)
    if path in b.LocalLB.VirtualServer.get_list():
        b.LocalLB.VirtualServer.delete_virtual_server([virtualname])
    else:
        print "Virtual Server '{}' not found".format(virtualname)


def delete_pool(b, pool_name):
    path = '/Common/{}'.format(pool_name)
    if path in b.LocalLB.Pool.get_list():
        b.LocalLB.Pool.delete_pool([pool_name])
    else:
        print "Pool '{}' not found.".format(pool_name)

def delete_nodes(b, pool_members):
    for member in pool_members:
        path = '/Common/{}'.format(member)
        if path in b.LocalLB.NodeAddressV2.get_list():
           b.LocalLB.NodeAddressV2.delete_node_address([member])
        else:
            print "Node '{}' not found".format(member)


if __name__ == '__main__':
    # makes connection to F5 Big IP
    try:
        b = bigsuds.BIGIP(
            hostname = '10.60.103.79', username='admin', password='cloudbolt', debug=True
        )
    except Exception, e:
        #set_progress("Error in connecting to F5 BIG-IP")
        pass

    virtualname = 'CloudBoltF5'
    pool_name = 'CloudBolt_Rocks'
    pool_members = ['52.24.240.88', '54.191.113.54']

    # functional process to delete load balancer in F5
    delete_virtual_server(b, virtualname)
    delete_pool(b, pool_name)
    delete_nodes(b, pool_members)

    #return "", "", ""
