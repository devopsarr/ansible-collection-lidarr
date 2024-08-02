#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: lidarr_root_folder

short_description: Manages Lidarr root folder.

version_added: "1.0.0"

description: Manages Lidarr root folder.

options:
    path:
        description: Actual root folder.
        required: true
        type: str
    name:
        description: Root folder friendly name.
        required: true
        type: str
    monitor_option:
        description: Monitor option.
        required: true
        type: str
        choices: [ "all", "future", "missing", "existing", "latest", "first", "none", "unknown" ]
    new_item_monitor_option:
        description: New item monitor option.
        required: true
        type: str
        choices: [ "all", "none", "new" ]
    metadata_profile_id:
        description: Metadata profile ID.
        required: true
        type: int
    quality_profile_id:
        description: Metadata profile ID.
        required: true
        type: int

extends_documentation_fragment:
    - devopsarr.lidarr.lidarr_credentials
    - devopsarr.lidarr.lidarr_state
    - devopsarr.lidarr.lidarr_taggable

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a root folder
- name: Create a root folder
  devopsarr.lidarr.root_folder:
    name: 'Music'
    path: '/music'
    new_item_monitor_option: 'all'
    monitor_option: 'all'
    metadata_profile_id: 1
    quality_profile_id: 1

# Delete a root folder
- name: Delete a root_folder
  devopsarr.lidarr.root_folder:
    name: 'Music'
    path: '/music'
    new_item_monitor_option: 'all'
    monitor_option: 'all'
    metadata_profile_id: 1
    quality_profile_id: 1
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: root folder ID.
    type: int
    returned: always
    sample: '1'
path:
    description: The root folder path.
    type: str
    returned: 'on create/update'
    sample: '/music'
name:
    description: Root folder friendly name.
    returned: always
    type: str
    sample: 'Name'
default_monitor_option:
    description: Monitor option.
    returned: always
    type: str
    sample: 'all'
default_new_item_monitor_option:
    description: New item monitor option.
    returned: always
    type: str
    sample: 'all'
default_metadata_profile_id:
    description: Metadata profile ID.
    returned: always
    type: int
    sample: 1
default_quality_profile_id:
    description: Metadata profile ID.
    returned: always
    type: int
    sample: 1
accessible:
    description: Access flag.
    type: str
    returned: 'on create/update'
    sample: 'true'
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


def is_changed(status, want):
    if (want.name != status.name or
            want.path != status.path or
            want.default_monitor_option != status.default_monitor_option or
            want.default_new_item_monitor_option != status.default_new_item_monitor_option or
            want.default_metadata_profile_id != status.default_metadata_profile_id or
            want.default_quality_profile_id != status.default_quality_profile_id or
            want.default_tags != status.default_tags):
        return True


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        path=dict(type='str', required=True),
        name=dict(type='str', required=True),
        state=dict(default='present', type='str', choices=['present', 'absent']),
        monitor_option=dict(type='str', choices=['all', 'future', 'missing', 'existing', 'latest', 'first', 'none', 'unknown'], required=True),
        new_item_monitor_option=dict(type='str', choices=['all', 'none', 'new'], required=True),
        metadata_profile_id=dict(type='int', required=True),
        quality_profile_id=dict(type='int', required=True),
        tags=dict(type='list', elements='int', default=[]),
    )


def create_root_folder(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.create_root_folder(root_folder_resource=want)
        except lidarr.ApiException as e:
            module.fail_json('Error creating root folder: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error creating root folder: {}'.format(to_native(e)), **result)
        result.update(response.model_dump(by_alias=False))
    module.exit_json(**result)


def list_root_folders(result):
    try:
        return client.list_root_folder()
    except lidarr.ApiException as e:
        module.fail_json('Error listing root folders: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing root folders: {}'.format(to_native(e)), **result)


def find_root_folder(path, result):
    for folder in list_root_folders(result):
        if folder.path == path:
            return folder
    return None


def update_root_folder(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.update_root_folder(root_folder_resource=want, id=str(want.id))
        except lidarr.ApiException as e:
            module.fail_json('Error updating root folder: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating root folder: {}'.format(to_native(e)), **result)
    # No need to exit module since it will exit by default either way
    result.update(response.model_dump(by_alias=False))


def delete_root_folder(result):
    if result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            try:
                client.delete_root_folder(result['id'])
            except lidarr.ApiException as e:
                module.fail_json('Error deleting root folder: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
            except Exception as e:
                module.fail_json('Error deleting root folder: {}'.format(to_native(e)), **result)
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
    client = lidarr.RootFolderApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Check if a resource is present already.
    state = find_root_folder(module.params['path'], result)
    if state:
        result.update(state.model_dump(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        delete_root_folder(result)

    # Set wanted resource.
    want = lidarr.RootFolderResource(
        path=module.params['path'],
        name=module.params['name'],
        default_monitor_option=module.params['monitor_option'],
        default_new_item_monitor_option=module.params['new_item_monitor_option'],
        default_metadata_profile_id=module.params['metadata_profile_id'],
        default_quality_profile_id=module.params['quality_profile_id'],
        default_tags=module.params['tags'],
    )

    # Create a new resource if needed.
    if result['id'] == 0:
        create_root_folder(want, result)

    # Update an existing resource.
    want.id = result['id']
    if is_changed(state, want):
        update_root_folder(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
