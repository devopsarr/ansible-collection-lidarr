#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: lidarr_release_profile_info

short_description: Get information about Lidarr release profile.

version_added: "1.0.0"

description: Get information about Lidarr release profile.

options:
    id:
        description: ID.
        type: int

extends_documentation_fragment:
    - devopsarr.lidarr.lidarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Gather information about all release profiles.
- name: Gather information about all release profiles
  devopsarr.lidarr.lidarr_release_profile_info:

# Gather information about a single release profile.
- name: Gather information about a single release profile
  devopsarr.lidarr.lidarr_release_profile_info:
    id: 1
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
release_profiles:
    description: A list of release profiles.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: Release Profile ID.
            type: int
            returned: always
            sample: 1
        ignored:
            description: Ignored terms. At least one of `required` and `ignored` must be set.
            type: list
            elements: str
            returned: always
            sample: ["proper", "repack"]
        required:
            description: Required terms. At least one of `required` and `ignored` must be set.
            type: list
            elements: str
            returned: always
            sample: ["proper", "repack"]
        indexer_id:
            description: Indexer ID. Set `0` for all."
            type: int
            returned: always
            sample: 1
        enabled:
            description: Enabled.
            type: bool
            returned: always
            sample: True
        tags:
            description: Tag list.
            type: list
            returned: always
            elements: int
            sample: [1,2]
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
        id=dict(type='int'),
    )


def list_release_profile(result):
    try:
        return client.list_release_profile()
    except Exception as e:
        module.fail_json('Error listing release profiles: %s' % to_native(e.reason), **result)


def populate_release_profile(result):
    profiles = []
    # Check if a resource is present already.
    for profile in list_release_profile(result):
        if module.params['id']:
            if profile.id == module.params['id']:
                profiles = [profile.model_dump(by_alias=False)]
        else:
            profiles.append(profile.model_dump(by_alias=False))
    return profiles


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = LidarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = lidarr.ReleaseProfileApi(module.api)
    result = dict(
        changed=False,
        release_profiles=[],
    )

    # List resources.
    result.update(release_profiles=populate_release_profile(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
