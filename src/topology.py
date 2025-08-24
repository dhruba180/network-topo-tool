# src/topology.py
import networkx as nx
import matplotlib.pyplot as plt

def build_graph(devices):
    G = nx.Graph()
    for dev_name, dev in devices.items():
        G.add_node(dev_name, **{'protocol': dev.get('protocol')})
    # find links by comparing networks
    dev_items = list(devices.items())
    for i in range(len(dev_items)):
        a_name, a_dev = dev_items[i]
        for j in range(i+1, len(dev_items)):
            b_name, b_dev = dev_items[j]
            for ai, ainf in a_dev['interfaces'].items():
                for bi, binf in b_dev['interfaces'].items():
                    if 'network' in ainf and 'network' in binf and ainf['network'] == binf['network']:
                        G.add_edge(a_name, b_name, interfaces=(ai, bi), network=ainf['network'],
                                   mtu_a=ainf.get('mtu'), mtu_b=binf.get('mtu'))
    return G

def visualize(G, filename=None):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=1200)
    edge_labels = {(u, v): d.get('network','') for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    if filename:
        plt.savefig(filename)
    plt.show()
