from network import Network
from graph import Graph

# Load the network
network_file = "examples/small.txt"
network = Network.from_file(network_file)
#print(network)
grp = network.build_extended_graph()
#print(grp)

