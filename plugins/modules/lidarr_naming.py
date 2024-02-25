#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: lidarr_naming

short_description: Manages Lidarr naming.

version_added: "1.0.0"

description: Manages Lidarr naming.

options:
    standard_track_format:
        description: Standard track format.
        required: true
        type: str
    multi_disc_track_format:
        description: Multi disc track format.
        required: true
        type: str
    artist_folder_format:
        description: Artist folder format.
        required: true
        type: str
    colon_replacement_format:
        description: Colon replacement format. 0 `delete`, 1 `dash`, 2 `spaceDash`, 3 `spaceDashSpace`, 4 `smart`.
        required: true
        type: int
        choices: [0, 1, 2, 3, 4]
    rename_tracks:
        description: Rename tracks.
        required: true
        type: bool
    replace_illegal_characters:
        description: Replace illegal characters.
        required: true
        type: bool

extends_documentation_fragment:
    - devopsarr.lidarr.lidarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# update naming
- name: Update naming
  devopsarr.lidarr.lidarr_naming:
    rename_tracks: true
    replace_illegal_characters: true
    colon_replacement_format: 1
    artist_folder_format: '{Artist Name}'
    multi_disc_track_format: '{Album Title} ({Release Year})/{Medium Format} {medium:00}/{Artist Name} - {Album Title} - {track:00} - {Track Title}'
    standard_track_format: '{Album Title} ({Release Year})/{Artist Name} - {Album Title} - {track:00} - {Track Title}'
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Naming ID.
    type: int
    returned: always
    sample: '1'
standard_track_format:
    description: Standard track format.
    returned: always
    type: str
    sample: '{Album Title} ({Release Year})/{Artist Name} - {Album Title} - {track:00} - {Track Title}'
multi_disc_track_format:
    description: Standard track format.
    returned: always
    type: str
    sample: '{Album Title} ({Release Year})/{Medium Format} {medium:00}/{Artist Name} - {Album Title} - {track:00} - {Track Title}'
artist_folder_format:
    description: Artist folder format.
    returned: always
    type: str
    sample: '{Artist Name}'
colon_replacement_format:
    description: Colon replacement format.
    returned: always
    type: int
    sample: 1
rename_tracks:
    description: Rename tracks.
    returned: always
    type: bool
    sample: true
replace_illegal_characters:
    description: Replace illegal characters.
    returned: always
    type: bool
    sample: true
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
        standard_track_format=dict(type='str', required=True),
        multi_disc_track_format=dict(type='str', required=True),
        artist_folder_format=dict(type='str', required=True),
        colon_replacement_format=dict(type='int', required=True, choices=[0, 1, 2, 3, 4]),
        rename_tracks=dict(type='bool', required=True),
        replace_illegal_characters=dict(type='bool', required=True),
    )


def read_naming(result):
    try:
        return client.get_naming_config()
    except Exception as e:
        module.fail_json('Error getting naming: %s' % to_native(e.reason), **result)


def update_naming(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.update_naming_config(naming_config_resource=want, id="1")
        except Exception as e:
            module.fail_json('Error updating naming: %s' % to_native(e.reason), **result)
    # No need to exit module since it will exit by default either way
    result.update(response.model_dump(by_alias=False))


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = LidarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )

    # Init client and result.
    client = lidarr.NamingConfigApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Get resource.
    state = read_naming(result)
    if state:
        result.update(state.model_dump(by_alias=False))

    want = lidarr.NamingConfigResource(
        standard_track_format=module.params['standard_track_format'],
        multi_disc_track_format=module.params['multi_disc_track_format'],
        artist_folder_format=module.params['artist_folder_format'],
        colon_replacement_format=module.params['colon_replacement_format'],
        rename_tracks=module.params['rename_tracks'],
        replace_illegal_characters=module.params['replace_illegal_characters'],
        id=1,
        # add not used parameters to compare resource
        include_quality=False,
        replace_spaces=False,
        include_artist_name=False,
        include_album_title=False,
    )

    # Update an existing resource.
    if want != state:
        update_naming(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
