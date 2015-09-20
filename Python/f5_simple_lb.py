#!/usr/bin/env python

import bigsuds
import time


b = bigsuds.BIGIP(hostname = '10.60.103.79', username='admin', password='cloudbolt', debug=True)
name = 'CloudBolt' + str(int(time.time()))

b.LocalLB.Pool.create_v2(
    ['/Common/{}'.format(name)],
    ['LB_METHOD_ROUND_ROBIN'],
    [[{'port':80, 'address':'172.31.45.156'},
    {'port':81, 'address':'1.2.3.4'}]]
)

"""
lbmeth = b.LocalLB.Pool.typefactory.create('LocalLB.LBMethod')
mem_sequence = b.LocalLB.Pool.typefactory.create('Common.IPPortDefinitionSequence')
mem1 = b.LocalLB.Pool.typefactory.create('Common.IPPortDefinition')
mem1.address = '172.31.45.156'
mem1.port = 80
mem_sequence.item = [mem1]
b.LocalLB.Pool.create(pool_names = [name], lb_methods = \
        [lbmeth.LB_METHOD_ROUND_ROBIN], members = [mem_sequence])
"""
