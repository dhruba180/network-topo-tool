# src/main.py
import json
from parser import parse_all
from topology import build_graph, visualize
from validator import find_duplicate_ips, find_mtu_mismatches, find_network_loops
from simulator import simulate_link_failure

def run(conf_dir='confs'):
    devices = parse_all(conf_dir)
    print("Parsed devices:", list(devices.keys()))
    G = build_graph(devices)
    print("Nodes:", G.nodes())
    print("Edges:", G.edges(data=True))
    # visualize
    visualize(G)
    # validations
    dups = find_duplicate_ips(devices)
    print("Duplicate IPs:", dups)
    mtus = find_mtu_mismatches(G)
    print("MTU mismatches:", mtus)
    loops = find_network_loops(G)
    print("Network loops:", loops)
    # simulate link failure example (first edge)
    if G.number_of_edges():
        u, v = list(G.edges())[0]
        comps = simulate_link_failure(G, u, v)
        print(f"Components after removing link {u}-{v}:", comps)

if __name__ == '__main__':
    run()