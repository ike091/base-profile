"""Spins up a variable number of nodes in a LAN. Based on the small-lan profile

Instructions:
Wait for the profile instance to start, and then log into nodes via the ssh ports specified.
"""

import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.emulab as emulab
import geni.rspec.igext as igext

# define some constants
UBUNTU18_IMG = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
CENTOS7_IMG = 'urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS7-64-STD'
SUPPORTED_HARDWARE_TYPES = ['pc3000', 'd430', 'd710']
SUPPORTED_MODES = ['slate_cluster', 'experiment']

# the number of extra public ip addresses to allocate
NUM_IP_ADDRESSES = 3

# create a portal context, needed to define parameters
pc = portal.Context()

# create a Request object to start building RSpec
request = pc.makeRequestRSpec()

# node count parameter
pc.defineParameter('node_count', 'Number of nodes', portal.ParameterType.INTEGER, 2)
pc.defineParameter('node_type_master', 'Type of physical node to instantiate master controller on', portal.ParameterType.STRING, 'd430')
pc.defineParameter('node_type_worker', 'Type of physical node to instantiate workers on (pc3000, d430, d710)', portal.ParameterType.STRING, 'd710')
pc.defineParameter('mode', 'Type of experiment to instantiate (slate_cluster or experiment)', portal.ParameterType.STRING, 'slate_cluster')

params = pc.bindParameters()

# validate node count
if params.node_count < 1:
    pc.reportError(portal.ParameterError('You must choose at least 1 node.', ['node_count']))

# validate hardware choices
if params.node_type_worker not in SUPPORTED_HARDWARE_TYPES:
    pc.reportError(portal.ParameterError('You must choose a valid hardware type.', ['node_type_worker']))
if params.node_type_master not in SUPPORTED_HARDWARE_TYPES:
    pc.reportError(portal.ParameterError('You must choose a valid hardware type.', ['node_type_master']))

# validate mode
if params.mode not in SUPPORTED_MODES:
    pc.reportError(portal.ParameterError('You must choose a valid operating system.', ['operating_system']))

pc.verifyParameters()

if params.node_count > 1:
    if params.node_count == 2:
        lan = request.Link()
    else:
        lan = request.LAN()


def run_install_script(this_node, script_name):
    """Runs a bash script from the install/ directory on a specific node."""

    this_node.addService(pg.Execute(shell='sh', command='chmod +x /local/repository/install/' + script_name))
    this_node.addService(pg.Execute(shell='sh', command='/local/repository/install/' + script_name))


for i in range(params.node_count):
    # create a node
    node = request.RawPC('node' + str(i))

    if params.node_count > 1:
        iface = node.addInterface('eth1')
        lan.addInterface(iface)

    # set the hardware type of each node in experiment mode
    if params.mode == 'experiment':
        if i == 0:
            node.hardware_type = params.node_type_master
        else:
            node.hardware_type = params.node_type_worker


    # set the OS on each node
    if params.mode == 'experiment':
        node.disk_image = UBUNTU18_IMG
    elif params.mode == 'slate_cluster':
        node.disk_image = CENTOS7_IMG

    # run different scripts based on mode
    if params.mode == 'experiment':
        # install management software on first node
        if i == 0:
            run_install_script(node, 'install_snmp_manager.sh')
            run_install_script(node, 'install_slate_cli.sh')
            run_install_script(node, 'install_minikube.sh')
            run_install_script(node, 'install_helm.sh')
            run_install_script(node, 'install_docker_compose.sh')
        # run install scripts on each node
        run_install_script(node, 'install_snmp_agent.sh')
        run_install_script(node, 'install_docker.sh')

    #  elif params.mode == 'slate_cluster':
        # put slate cluster specific install scripts and configuration here (CentOS7)
        #  if i == 0:
            #  run_install_script(node, 'install_kubernetes_cluster.sh')
        #  else:
            #  run_install_script(node, 'install_kubernetes_worker_node.sh')


# request a pool of dynamic publically routable ip addresses
address_pool = igext.AddressPool('address_pool', NUM_IP_ADDRESSES)
address_pool.component_manager_id = ('urn:publicid:IDN+utah.cloudlab.us+authority+cm')
request.addResource(address_pool)

# output RSpec
pc.printRequestRSpec(request)
