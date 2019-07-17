from sys import exit, stderr
import json

import esxi

options, args = esxi.parse_options('Usage: %prog [options] -H ESXI_HOST -u ESXI_USER PORTGROUP_NAME')

if len(args) == 0:
    print('"PORTGROUP_NAME" is required', file=stderr)
    exit(1)

portgroup = args[0]

client = esxi.Client(host=options.host, user=options.user, password=options.password)
mac_addresses = []

for vm in client.vms:
    for intf in vm.interfaces:
        if intf.deviceInfo.summary != portgroup:
            continue

        mac_addresses.append({
            'host': vm.name,
            'interface': intf.deviceInfo.label,
            'mac_address': intf.macAddress})

print(json.dumps(mac_addresses))
