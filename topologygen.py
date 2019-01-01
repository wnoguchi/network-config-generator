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

params = {
    'nodes': [
        {
            'index': 1,
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
            'index': 2,
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
        {
            'index': 3,
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
                    'address': '100.1.{{ index }}.{{ index }}',
                    'mask': mask24,
                },
                {
                    'name': 'GigabitEthernet 0/1',
                    'address': '100.{{ index }}.5.{{ index }}',
                    'mask': mask24,
                },
                {
                    'name': 'GigabitEthernet 0/2',
                    'address': '100.{{ index }}.4.{{ index }}',
                    'mask': mask24,
                },
            ]
        },
        {
            'index': 4,
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
                    'address': '10.{{ index }}.5.{{ index }}',
                    'mask': mask24,
                },
                {
                    'name': 'GigabitEthernet 0/1',
                    'address': '100.2.{{ index }}.{{ index }}',
                    'mask': mask24,
                },
                {
                    'name': 'GigabitEthernet 0/2',
                    'address': '10.3.{{ index }}.{{ index }}',
                    'mask': mask24,
                },
            ]
        },
        {
            'index': 5,
            'vendor': 'cisco',
            'node_type': 'router',
            'interfaces': [
                {
                    'name': 'Loopback 1',
                    'address': '{{ index }}.{{ index }}.{{ index }}.{{ index }}',
                    'mask': mask32,
                },
                {
                    'name': 'Loopback 2',
                    'address': '30.0.0.{{ index }}',
                    'mask': mask16,
                },
                {
                    'name': 'GigabitEthernet 0/0',
                    'address': '10.3.{{ index }}.{{ index }}',
                    'mask': mask24,
                },
                {
                    'name': 'GigabitEthernet 0/1',
                    'address': '10.4.{{ index }}.{{ index }}',
                    'mask': mask24,
                },
            ]
        },
        {
            'index': 6,
            'vendor': 'cisco',
            'node_type': 'router',
            'interfaces': [
                {
                    'name': 'Loopback 1',
                    'address': '{{ index }}.{{ index }}.{{ index }}.{{ index }}',
                    'mask': mask32,
                },
                {
                    'name': 'Loopback 2',
                    'address': '50.0.0.{{ index }}',
                    'mask': mask16,
                },
                {
                    'name': 'GigabitEthernet 0/0',
                    'address': '100.2.{{ index }}.{{ index }}',
                    'mask': mask24,
                },
                {
                    'name': 'GigabitEthernet 0/1',
                    'address': '100.1.{{ index }}.{{ index }}',
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
