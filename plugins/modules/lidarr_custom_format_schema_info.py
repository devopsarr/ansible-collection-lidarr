#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: lidarr_custom_format_schema_info

short_description: Get information about Lidarr custom format schema.

version_added: "1.0.0"

description: Get information about Lidarr custom format schema.

options:
    name:
        description: Name.
        type: str

extends_documentation_fragment:
    - devopsarr.lidarr.lidarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Gather information about all custom formats schema.
- name: Gather information about all custom formats schema
  devopsarr.lidarr.lidarr_custom_format_schema_info:

# Gather information about a single custom format schema.
- name: Gather information about a single custom format schema
  devopsarr.lidarr.lidarr_custom_format_schema_info:
    name: test
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
custom_formats:
    description: A list of custom format.
    returned: always
    type: list
    elements: dict
    contains:
        config_contract:
            description: Config contract.
            returned: always
            type: str
            sample: "BroadcastheNetSettings"
        implementation:
            description: Implementation.
            returned: always
            type: str
            sample: "BroadcastheNet"
        fields:
            description: field list.
            type: list
            returned: always
'''

from ansible_collections.devopsarr.lidarr.plugins.module_utils.lidarr_module import LidarrModule
from ansible.module_utils.common.text.converters import to_native

try:
    import lidarr
    HAS_LIDARR_LIBRARY = True
except ImportError:
    HAS_LIDARR_LIBRARY = False


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        name=dict(type='str'),
    )


def list_custom_format_schema(result):
    try:
        return client.list_custom_format_schema()
    except Exception as e:
        module.fail_json('Error listing custom formats: %s' % to_native(e.reason), **result)


def populate_custom_format_schema(result):
    custom_formats = []
    # Check if a resource is present already.
    for custom_format in list_custom_format_schema(result):
        if module.params['name']:
            if custom_format.implementation == module.params['name']:
                custom_formats = [custom_format.model_dump(by_alias=False)]
        else:
            custom_formats.append(custom_format.model_dump(by_alias=False))
    return custom_formats


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = LidarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = lidarr.CustomFormatApi(module.api)
    result = dict(
        changed=False,
        custom_formats=[],
    )

    # List resources.
    result.update(custom_formats=populate_custom_format_schema(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
