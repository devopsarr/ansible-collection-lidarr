#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: lidarr_quality_info

short_description: Get information about Lidarr quality.

version_added: "1.0.0"

description: Get information about Lidarr quality.

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
# fetch all qualities
- name: fetch all qualities
  devopsarr.lidarr.lidarr_quality_info:

# fetch a single quality
- name: fetch a single quality
  devopsarr.lidarr.lidarr_quality_info:
    name: FLAC
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
qualities:
    description: A list of quality.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: Quality ID.
            type: int
            returned: always
            sample: '1'
        title:
            description: Title.
            returned: always
            type: str
            sample: 'WEBRip-480p'
        min_size:
            description: Minimum size.
            returned: always
            type: float
            sample: '1.0'
        max_size:
            description: Maximum size.
            returned: always
            type: float
            sample: '130.0'
        quality:
            description: Music folder format.
            returned: always
            type: dict
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


def list_qualities(result):
    try:
        return client.list_quality_definition()
    except lidarr.ApiException as e:
        module.fail_json('Error getting qualities: {}\n body {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error getting qualities: {}'.format(to_native(e)), **result)


def populate_qualities(result):
    qualities = []
    # Check if a resource is present already.
    for quality in list_qualities(result):
        if module.params['name']:
            if quality.quality.name == module.params['name']:
                qualities = [quality.model_dump(by_alias=False)]
        else:
            qualities.append(quality.model_dump(by_alias=False))
    return qualities


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = LidarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = lidarr.QualityDefinitionApi(module.api)
    result = dict(
        changed=False,
        qualities=[],
    )

    # List resources.
    result.update(qualities=populate_qualities(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
