import json


class Node(object):
    all = {}

    @classmethod
    def add(cls, name, interfaces):
        cls.all[name] = cls.all.get(
            name,
            cls(
                name,
                [(i.deviceInfo.label, Network.get(i.deviceInfo.summary)) for i in interfaces]))

    @classmethod
    def reset(cls):
        cls.all = {}

    def __init__(self, name, interfaces):
        self.name = name
        self.interfaces = dict(interfaces)

        for intf_name, network in interfaces:
            network.connect(self)

    def facing_interface(self, network):
        return [intf_name for intf_name, net in self.interfaces.items() if net == network][0]


class Network(object):
    all = {}

    @classmethod
    def add(cls, portgroup):
        cls.all[portgroup.spec.name] = cls.all.get(portgroup.spec.name,
                                                   cls(portgroup.spec.name, portgroup.spec.vlanId))

    @classmethod
    def get(cls, name):
        return cls.all.get(name, None)

    @classmethod
    def reset(cls):
        cls.all = {}

    def __init__(self, name, vlan_id):
        self.name = name
        self.vlan_id = vlan_id
        self.nodes = []

    def connect(self, node):
        self.nodes.append(node)


class Dumper(object):
    def __init__(self, client):
        self.client = client

    def preprocess(self):
        Node.reset()
        Network.reset()

        for pg in self.client.portgroups:
            Network.add(pg)

        for vm in self.client.vms:
            Node.add(vm.name, self.client.interfaces(vm))

    def dump(self):
        self.preprocess()

        nodes = [{'name': name, 'icon': 'https://inet-henge.herokuapp.com/images/router.png'}
                 for name, node in Node.all.items()]
        links = []

        done = []
        for name, node in Node.all.items():
            for intf_name, network in node.interfaces.items():
                if len(network.nodes) != 2:  # Pick up p2p links only
                    continue

                other = [n for n in network.nodes if n != node][0]
                if {node, other} in done:
                    continue

                links.append({'source': name,
                              'target': other.name,
                              'meta': {'interface': {'source': intf_name,
                                                     'target': other.facing_interface(network)},
                                       'vlan_id': 'Vlan ID: %d' % network.vlan_id}})
                done.append({node, other})

        return json.dumps({
            'nodes': nodes,
            'links': links})
