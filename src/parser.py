# src/parser.py
import re, os, json
from ipaddress import IPv4Network

def parse_config_file(path):
    with open(path) as f:
        txt = f.read()
    hostname_m = re.search(r'^hostname\s+(\S+)', txt, re.M)
    hostname = hostname_m.group(1) if hostname_m else os.path.splitext(os.path.basename(path))[0]

    interfaces = {}
    for m in re.finditer(r'interface\s+(\S+)([\s\S]*?)(?=\ninterface\s|\nhostname\s|\nrouter\s|\Z)', txt):
        name = m.group(1)
        body = m.group(2)
        ip_m = re.search(r'ip address\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)', body)
        mtu_m = re.search(r'mtu\s+(\d+)', body)
        desc_m = re.search(r'description\s+(.+)', body)
        entry = {}
        if ip_m:
            ip = ip_m.group(1); mask = ip_m.group(2)
            try:
                net = IPv4Network(f"{ip}/{mask}", strict=False)
                entry['ip'] = f"{ip}/{net.prefixlen}"
                entry['network'] = f"{net.network_address}/{net.prefixlen}"
            except Exception:
                entry['ip'] = ip
        if mtu_m:
            entry['mtu'] = int(mtu_m.group(1))
        if desc_m:
            entry['description'] = desc_m.group(1).strip()
        interfaces[name] = entry

    proto = None
    if re.search(r'^router ospf', txt, re.M):
        proto = 'ospf'
    elif re.search(r'^router bgp', txt, re.M):
        proto = 'bgp'

    return {'hostname': hostname, 'interfaces': interfaces, 'protocol': proto}

def parse_all(conf_dir='confs'):
    devices = {}
    for fname in os.listdir(conf_dir):
        if not fname.endswith('.cfg') and not fname.endswith('.dump'): 
            continue
        path = os.path.join(conf_dir, fname)
        dev = parse_config_file(path)
        devices[dev['hostname']] = dev
    return devices

if __name__ == '__main__':
    import pprint
    print(pprint.pformat(parse_all()))