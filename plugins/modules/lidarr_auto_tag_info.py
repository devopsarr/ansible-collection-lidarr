#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: lidarr_auto_tag_info

short_description: Get information about Lidarr auto tag.

version_added: "1.0.0"

description: Get information about Lidarr auto tag.

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
# Gather information about all auto tags
- name: Gather information about all auto tags
  devopsarr.lidarr.lidarr_auto_tag_info:

# Gather information about a single auto tag
- name: Gather information about a single auto tag
  devopsarr.lidarr.lidarr_auto_tag_info:
    name: Example
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
auto_tags:
    description: A list of auto tag.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: auto tagID.
            type: int
            returned: always
            sample: 1
        name:
            description: Name.
            returned: always
            type: str
            sample: "Example"
        remove_tags_automatically:
            description: Include auto tag when renaming flag.
            returned: always
            type: bool
            sample: false
        tags:
            description: Tag list.
            type: list
            returned: always
            elements: int
            sample: [1,2]
        specifications:
            description: specification list.
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


def list_auto_tags(result):
    try:
        return client.list_auto_tagging()
    except lidarr.ApiException as e:
        module.fail_json('Error listing auto tags: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing auto tags: {}'.format(to_native(e)), **result)


def populate_auto_tags(result):
    auto_tags = []
    # Check if a resource is present already.
    for auto_tag in list_auto_tags(result):
        if module.params['name']:
            if auto_tag.name == module.params['name']:
                auto_tags = [auto_tag.model_dump(by_alias=False)]
        else:
            auto_tags.append(auto_tag.model_dump(by_alias=False))
    return auto_tags


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = LidarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = lidarr.AutoTaggingApi(module.api)
    result = dict(
        changed=False,
        auto_tags=[],
    )

    # List resources.
    result.update(auto_tags=populate_auto_tags(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
