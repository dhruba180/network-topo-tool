# src/validator.py
import networkx as nx

def find_duplicate_ips(devices):
    ip_map = {}
    duplicates = []
    for dev, info in devices.items():
        for intf, data in info['interfaces'].items():
            if 'ip' in data:
                ip = data['ip'].split('/')[0]
                if ip in ip_map:
                    duplicates.append((ip, ip_map[ip], f"{dev}:{intf}"))
                else:
                    ip_map[ip] = f"{dev}:{intf}"
    return duplicates

def find_mtu_mismatches(G):
    mismatches = []
    for u, v, d in G.edges(data=True):
        if d.get('mtu_a') and d.get('mtu_b') and d['mtu_a'] != d['mtu_b']:
            mismatches.append((u, v, d['mtu_a'], d['mtu_b']))
    return mismatches

def find_network_loops(G):
    # cycles in graph -> loops
    cycles = nx.cycle_basis(G)
    return cycles
