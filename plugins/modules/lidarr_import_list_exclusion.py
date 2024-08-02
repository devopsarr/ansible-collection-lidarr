#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: lidarr_import_list_exclusion

short_description: Manages Lidarr import list exclusion.

version_added: "1.0.0"

description: Manages Lidarr import list exclusion.

options:
    foreign_id:
        description: Foreign ID.
        required: true
        type: str
    artist_name:
        description: Artist name.
        required: true
        type: str

extends_documentation_fragment:
    - devopsarr.lidarr.lidarr_credentials
    - devopsarr.lidarr.lidarr_state

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a import list exclusion
- name: Create a import list exclusion
  devopsarr.lidarr.lidarr_import_list_exclusion:
    foreign_id: "b1a9c0e9-d987-4042-ae91-78d6a3267d69"
    artist_name: "test"


# Delete a import list exclusion
- name: Delete a import_list_exclusion
  devopsarr.lidarr.lidarr_import_list_exclusion:
    foreign_id: "b1a9c0e9-d987-4042-ae91-78d6a3267d69"
    artist_name: "test"
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: import list exclusion ID.
    type: int
    returned: always
    sample: 1
foreign_id:
    description: Foreign ID.
    type: str
    returned: 'always'
    sample: "b1a9c0e9-d987-4042-ae91-78d6a3267d69"
artist_name:
    description: Foreign ID.
    type: str
    returned: 'always'
    sample: "Queen"
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
        foreign_id=dict(type='str', required=True),
        artist_name=dict(type='str', required=True),
        state=dict(default='present', type='str', choices=['present', 'absent']),
    )


def create_import_list_exclusion(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.create_import_list_exclusion(import_list_exclusion_resource=want)
        except lidarr.ApiException as e:
            module.fail_json('Error creating import list exclusion: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error creating import list exclusion: {}'.format(to_native(e)), **result)
        result.update(response.model_dump(by_alias=False))
    module.exit_json(**result)


def list_import_list_exclusions(result):
    try:
        return client.list_import_list_exclusion()
    except lidarr.ApiException as e:
        module.fail_json('Error listing import list exclusions: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing import list exclusions: {}'.format(to_native(e)), **result)


def find_import_list_exclusion(artist_name, foreign_id, result):
    for import_list_exclusion in list_import_list_exclusions(result):
        if import_list_exclusion.foreign_id == foreign_id and \
           import_list_exclusion.artist_name == artist_name:
            return import_list_exclusion
    return None


def delete_import_list_exclusion(result):
    if result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            try:
                client.delete_import_list_exclusion(result['id'])
            except lidarr.ApiException as e:
                module.fail_json('Error deleting import list exclusion: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
            except Exception as e:
                module.fail_json('Error deleting import list exclusion: {}'.format(to_native(e)), **result)
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
    client = lidarr.ImportListExclusionApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Check if a resource is present already.
    state = find_import_list_exclusion(module.params['artist_name'], module.params['foreign_id'], result)
    if state:
        result.update(state.model_dump(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        delete_import_list_exclusion(result)

    # Set wanted resource.
    want = lidarr.ImportListExclusionResource(
        foreign_id=module.params['foreign_id'],
        artist_name=module.params['artist_name'],
    )

    # Create a new resource if needed.
    if result['id'] == 0:
        create_import_list_exclusion(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
