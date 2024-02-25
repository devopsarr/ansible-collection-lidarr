#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: lidarr_release_profile

short_description: Manages Lidarr release profile.

version_added: "1.0.0"

description: Manages Lidarr release profile.

options:
    ignored:
        description: Ignored terms. At least one of `required` and `ignored` must be set.
        type: list
        elements: str
    required:
        description: Required terms. At least one of `required` and `ignored` must be set.
        type: list
        elements: str
    indexer_id:
        description: Indexer ID. Set `0` for all.
        type: int
        default: 0
    enabled:
        description: Enabled.
        type: bool

extends_documentation_fragment:
    - devopsarr.lidarr.lidarr_credentials
    - devopsarr.lidarr.lidarr_taggable
    - devopsarr.lidarr.lidarr_state

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a release profile
- name: Create a release profile
  devopsarr.lidarr.lidarr_release_profile:
    enabled: true
    required: ["proper"]
    ignored: ["repack"]
    indexer_id: 1
    tags: [1,2]

# Delete a release profile
- name: Delete a release_profile
  devopsarr.lidarr.lidarr_release_profile:
    enabled: true
    required: ["proper"]
    ignored: ["repack"]
    indexer_id: 1
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
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
        ignored=dict(type='list', elements='str'),
        required=dict(type='list', elements='str'),
        indexer_id=dict(type='int', default=0),
        enabled=dict(type='bool'),
        tags=dict(type='list', elements='int', default=[]),
        state=dict(default='present', type='str', choices=['present', 'absent']),
    )


def create_release_profile(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.create_release_profile(release_profile_resource=want)
        except Exception as e:
            module.fail_json('Error creating release profile: %s' % to_native(e.reason), **result)
        result.update(response.model_dump(by_alias=False))
    module.exit_json(**result)


def list_release_profiles(result):
    try:
        return client.list_release_profile()
    except Exception as e:
        module.fail_json('Error listing release profiles: %s' % to_native(e.reason), **result)


def find_release_profile(want, result):
    for profile in list_release_profiles(result):
        if (profile.enabled == want.enabled and
                profile.required == want.required and
                profile.ignored == want.ignored and
                profile.indexer_id == want.indexer_id and
                profile.tags == want.tags):
            return profile
    return None


def delete_release_profile(result):
    if result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            try:
                client.delete_release_profile(result['id'])
            except Exception as e:
                module.fail_json('Error deleting release profile: %s' % to_native(e.reason), **result)
            result['id'] = 0
    module.exit_json(**result)


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
        id=0,
    )

    # Set wanted resource.
    want = lidarr.ReleaseProfileResource(
        enabled=module.params['enabled'],
        required=module.params['required'],
        ignored=module.params['ignored'],
        indexer_id=module.params['indexer_id'],
        tags=module.params['tags'],
    )

    # Check if a resource is present already.
    state = find_release_profile(want, result)
    if state:
        result.update(state.model_dump(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        delete_release_profile(result)

    # Create a new resource if needed.
    if result['id'] == 0:
        create_release_profile(want, result)

    # No update is possible without a name to identify the profile.
    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
