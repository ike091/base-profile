"""Spins up a variable number of nodes in a LAN. Based on the small-lan profile

Instructions:
Wait for the profile instance to start, and then log into nodes via the ssh ports specified.
"""

import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.emulab as emulab

# define some constants
UBUNTU18_IMG = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
SUPPORTED_HARDWARE_TYPES = ['pc3000', 'd430', 'd710']

# create a portal context, needed to define parameters
pc = portal.Context()

# create a Request object to start building RSpec
request = pc.makeRequestRSpec()

# node count parameter
pc.defineParameter('node_count', 'Number of nodes', portal.ParameterType.INTEGER, 2)
pc.defineParameter('node_type_master', 'Type of physical node to instantiate master controller on', portal.ParameterType.STRING, 'd710')
pc.defineParameter('node_type_worker', 'Type of physical node to instantiate workers on (pc3000, d430, d710)', portal.ParameterType.STRING, 'pc3000')

params = pc.bindParameters()

# validate node count
if params.node_count < 1:
    pc.reportError(portal.ParameterError('You must choose at least 1 node.', ['node_count']))

# validate hardware choices
if params.node_type_worker not in SUPPORTED_HARDWARE_TYPES:
    pc.reportError(portal.ParameterError('You must choose a valid hardware type.', ['node_type_worker']))
if params.node_type_master not in SUPPORTED_HARDWARE_TYPES:
    pc.reportError(portal.ParameterError('You must choose a valid hardware type.', ['node_type_master']))

pc.verifyParameters()

if params.node_count > 1:
    if params.node_count == 2:
        lan = request.Link()
    else:
        lan = request.LAN()


def run_bash_script(this_node, script_name):
    """Runs a bash script on a specific node."""

    this_node.addService(pg.Execute(shell='sh', command='chmod +x /local/repository/' + script_name))
    this_node.addService(pg.Execute(shell='sh', command='/local/repository/' + script_name))


for i in range(params.node_count):
    # create a node
    node = request.RawPC('node' + str(i))

    if params.node_count > 1:
        iface = node.addInterface('eth1')
        lan.addInterface(iface)

    # set the hardware type of each node
    if i == 0:
        node.hardware_type = params.node_type_master
    else:
        node.hardware_type = params.node_type_worker


    # set the OS on each node
    node.disk_image = UBUNTU18_IMG

    # install management software on first node
    if i == 0:
        run_bash_script(node, 'install_snmp_manager.sh')

    # run install scripts on each node
    run_bash_script(node, 'install_snmp_agent.sh')
    run_bash_script(node, 'install_docker.sh')


# output RSpec
pc.printRequestRSpec(request)
