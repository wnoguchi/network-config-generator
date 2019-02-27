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
                    'address': '100.1.6.1',
                    'mask': mask24,
                },
                {
                    'name': 'GigabitEthernet 0/1',
                    'address': '100.1.3.1',
                    'mask': mask24,
                },
            ],
            'routes': [
                {
                    'network': '6.6.6.6',
                    'mask': mask32,
                    'next_hop': '100.1.6.6',
                },
                {
                    'network': '3.3.3.3',
                    'mask': mask32,
                    'next_hop': '100.1.3.3',
                },
            ],
            'router': [
                {
                    'routing_protocol': 'bgp',
                    'as_number': 1,
                    'neighbors': [
                        {
                            'address': '100.1.6.6',
                            'remote-as': '50'
                        },
                        {
                            'address': '100.1.3.3',
                            'remote-as': '3'
                        },
                    ]
                }
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
                    'address': '100.{{ index }}.4.{{ index }}',
                    'mask': mask24,
                },
                {
                    'name': 'GigabitEthernet 0/1',
                    'address': '100.{{ index }}.6.{{ index }}',
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
                    'address': '100.1.3.3',
                    'mask': mask24,
                },
                {
                    'name': 'GigabitEthernet 0/1',
                    'address': '10.3.5.3',
                    'mask': mask24,
                },
                {
                    'name': 'GigabitEthernet 0/2',
                    'address': '10.3.4.3',
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
                    'address': '10.4.5.4',
                    'mask': mask24,
                },
                {
                    'name': 'GigabitEthernet 0/1',
                    'address': '100.2.4.4',
                    'mask': mask24,
                },
                {
                    'name': 'GigabitEthernet 0/2',
                    'address': '10.3.4.4',
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
                    'address': '30.0.0.5',
                    'mask': mask16,
                },
                {
                    'name': 'GigabitEthernet 0/0',
                    'address': '10.3.5.5',
                    'mask': mask24,
                },
                {
                    'name': 'GigabitEthernet 0/1',
                    'address': '10.4.5.5',
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
                    'address': '50.0.0.6',
                    'mask': mask16,
                },
                {
                    'name': 'GigabitEthernet 0/0',
                    'address': '100.2.6.6',
                    'mask': mask24,
                },
                {
                    'name': 'GigabitEthernet 0/1',
                    'address': '100.1.6.6',
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
