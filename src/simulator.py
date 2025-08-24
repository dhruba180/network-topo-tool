# src/simulator.py
import networkx as nx
from queue import Queue
from threading import Thread

def simulate_link_failure(G, node_a, node_b):
    if not G.has_edge(node_a, node_b):
        print("Edge not present")
        return
    G_removed = G.copy()
    G_removed.remove_edge(node_a, node_b)
    # check connectivity / affected nodes
    components = list(nx.connected_components(G_removed))
    return components

# threading skeleton
class VirtualDevice(Thread):
    def __init__(self, name, inbox):
        super().__init__(daemon=True)
        self.name = name
        self.inbox = inbox
        self.running = True
    def run(self):
        while self.running:
            msg = self.inbox.get()
            if msg == 'STOP':
                self.running = False
                break
            # process metadata (for MVP just print)
            print(f"[{self.name}] received: {msg}")
