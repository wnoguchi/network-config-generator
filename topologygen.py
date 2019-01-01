#/usr/bin/env python3

import copy
from jinja2 import Environment, FileSystemLoader, Template

env = Environment(loader=FileSystemLoader('templates/'))
#env = Environment()
node_template = env.get_template('cisco/router.j2')
output_template = env.get_template('output-templates/dokuwiki.j2')

mask24 = '255.255.255.0'
mask32 = '255.255.255.255'

params = {
    'nodes': [
        {
            'vendor': 'cisco',
            'node_type': 'router',
            'interfaces': [
                {
                    'name': 'Loopback 1',
                    'address': '{{ index }}.{{ index }}.{{ index }}.{{ index }}',
                    'mask': mask32,
                },
                {
                    'name': 'GigabitEthernet 0/0',
                    'address': '100.{{ index }}.6.{{ index }}',
                    'mask': mask24,
                },
                {
                    'name': 'GigabitEthernet 0/1',
                    'address': '100.{{ index }}.3.{{ index }}',
                    'mask': mask24,
                },
            ]
        },
        {
            'vendor': 'cisco',
            'node_type': 'router',
            'interfaces': [
                {
                    'name': 'Loopback 1',
                    'address': '{{ index }}.{{ index }}.{{ index }}.{{ index }}',
                    'mask': mask32,
                },
                {
                    'name': 'GigabitEthernet 0/0',
                    'address': '100.{{ index }}.2.{{ index }}',
                    'mask': mask24,
                },
                {
                    'name': 'GigabitEthernet 0/1',
                    'address': '100.{{ index }}.4.{{ index }}',
                    'mask': mask24,
                },
            ]
        },
    ]
}

render_params = copy.deepcopy(params)

i = 1
for node in render_params['nodes']:
    node['hostname'] = 'R%d' % i
    for interface in node['interfaces']:
        interface['address'] = Template(interface['address']).render({'index': i})
    i += 1

output_render_data = copy.deepcopy(render_params)

#{**x, **y}

for node in output_render_data['nodes']:
    node['config'] = node_template.render(node)

print(output_template.render(output_render_data))
