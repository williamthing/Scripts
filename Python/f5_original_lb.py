#!/usr/bin/env python

import bigsuds
import time
import sys

def create_pool(obj, pool, lbmethod, pl_mems):
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
        pllist = obj.LocalLB.Pool.get_list()
        if pool in pllist:
            obj.LocalLB.Pool.add_member_v2([pool], [pmlist])
        else:
            obj.LocalLB.Pool.create_v2([pool],[lbmethod],[pmlist])

        return obj.LocalLB.Pool.get_member_v2([pool])
    except Exception, e:
        print e


if __name__ == "__main__":
    try:
        b = bigsuds.BIGIP(
            hostname = '10.60.103.79', username='admin', password='cloudbolt', debug=True
        )
    except Exception, e:
        print "Error in connecting to F5 BIG-IP"

    name = 'CloudBolt_Rocks'
    #name = 'CloudBolt' + str(int(time.time()))
    lb_meth = 'LB_METHOD_ROUND_ROBIN'
    server = []
    if len(sys.argv) < 2:
        server = [{'52.24.37.208': 80}]
    else:
        i = 1
        # using for debugging
        print len(sys.argv)
        while i < len(sys.argv):
            server.append({sys.argv[i]: 80})
            i += 1

    poolinfo = create_pool(b, name, lb_meth, server)
    for x in poolinfo:
        print "Pool: {}".format(name)
        for y in x:
            print "\t%s:%d" % (y['address'], y['port'])
