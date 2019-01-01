#/usr/bin/env python3

import copy
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates/'))
#env = Environment()
template = env.get_template('bgp-topology.j2')

params = {
    'nodes': [
        {
            'node_type': 'router',
            'interfaces': [
                'gig0/1': {
                }
            ]
        },
    ]
}

render_params = copy.deepcopy(params)

for node in render_params.nodes:
    node


print(template.render(render_params))
