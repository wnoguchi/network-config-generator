#/usr/bin/env python3

import copy
from jinja2 import Environment, FileSystemLoader, Template

env = Environment(loader=FileSystemLoader('templates/'))
#env = Environment()
node_template = env.get_template('cisco/router.j2')
output_template = env.get_template('output-templates/dokuwiki.j2')

mask16 = '255.255.0.0'
mask24 = '255.255.255.0'
mask32 = '255.255.255.255'

number_of_routers = 4
number_of_loopback_interfaces = 0
number_of_gigabit_ethernet_interfaces = 2



# render_params = copy.deepcopy(params)

loBase = 1
gigBase = 0

render_params = {
    'nodes': [],
}

i = 1
for node in range(number_of_routers):
    node = {}
    render_params['nodes'].append(node)
    node['hostname'] = 'R%d' % i
    node['interfaces'] = []
    interfaceIndex = 0
    for loIndex in range(number_of_loopback_interfaces):
        node['interfaces'].append({
            'name': 'Loopback %d' % (loBase + loIndex),
            'address': '100.10.%d.1' % (loBase + loIndex),
            'mask': mask24,
        })
    for gigIndex in range(number_of_gigabit_ethernet_interfaces):
        node['interfaces'].append({
            'name': 'GigabitEthernet 0/%d' % (gigBase + gigIndex),
            'address': '0.0.0.0',
            'mask': mask24,
        })
    i += 1

output_render_data = copy.deepcopy(render_params)

#{**x, **y}

for node in output_render_data['nodes']:
    node['config'] = node_template.render(node)

print(output_template.render(output_render_data))
