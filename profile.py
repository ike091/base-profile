"""Spins up a variable number of nodes in a LAN. Based on the small-lan profile

Instructions:
Wait for the profile instance to start, and then log into nodes via the ssh ports specified.
"""

import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.emulab as emulab

# create a portal context, needed to define parameters
pc = portal.Context()

# create a Request object to start building RSpec
request = pc.makeRequestRSpec()

# node count parameter
pc.defineParameter('node_count', 'Number of nodes', portal.ParameterType.INTEGER, 2)


UBUNTU18_IMG = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'

params = pc.bindParameters()

if params.node_count < 1:
    pc.reportError(portal.ParameterError('You must choose at least 1 node.', ['node_count']))

pc.verifyParameters()

if params.node_count > 1:
    if params.node_count == 2:
        lan = request.Link()
    else:
        lan = request.LAN()

for i in range(params.node_count):
    # create a node
    node = request.RawPC('node' + str(i))

    if params.node_count > 1:
        iface = node.addInterface('eth1')
        lan.addInterface(iface)

    # set the hardware type of each node
    node.hardware_type = HARDWARE_TYPE

    # set the OS on each node
    node.disk_image = UBUNTU18_IMG


# output RSpec
pc.printRequestRSpec(request)
