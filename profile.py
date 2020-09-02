"""Spins up a variable number of nodes in a LAN. Based on the small-lan profile

Instructions:
Wait for the profile instance to start, and then log into nodes via the ssh ports specified.
"""

import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.emulab as emulab

# define some constants
UBUNTU18_IMG = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
HARDWARE_TYPE = "pc3000"

# create a portal context, needed to define parameters
pc = portal.Context()

# create a Request object to start building RSpec
request = pc.makeRequestRSpec()

# node count parameter
pc.defineParameter('node_count', 'Number of nodes', portal.ParameterType.INTEGER, 2)

params = pc.bindParameters()

if params.node_count < 1:
    pc.reportError(portal.ParameterError('You must choose at least 1 node.', ['node_count']))

pc.verifyParameters()

if params.node_count > 1:
    if params.node_count == 2:
        lan = request.Link()
    else:
        lan = request.LAN()


def run_bash_script(this_node, script_name):
    """Runs a bash script on a specific node."""

    this_node.addService(pg.Execute(shell='sh', command='chmod +x /local/repository/' + script_name))
    node.addService(pg.Execute(shell='sh', command='/local/repository/' + script_name))


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

    # install management software on first node
    if i == 0:
        run_bash_script(node, 'install_snmp_manager.sh')

    # run install scripts on each node
    run_bash_script(node, 'install_snmp_agent.sh')
    run_bash_script(node, 'install_docker.sh')


# output RSpec
pc.printRequestRSpec(request)
