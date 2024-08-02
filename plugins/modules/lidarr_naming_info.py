#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: lidarr_naming_info

short_description: Get information about Lidarr naming.

version_added: "1.0.0"

description: Get information about Lidarr naming.

extends_documentation_fragment:
    - devopsarr.lidarr.lidarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# fetch naming
- name: fetch naming
  devopsarr.lidarr.lidarr_naming_info:
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


def get_naming_config(result):
    try:
        return client.get_naming_config()
    except lidarr.ApiException as e:
        module.fail_json('Error getting naming: {}\n body {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error getting naming: {}'.format(to_native(e)), **result)


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = LidarrModule(
        argument_spec={},
        supports_check_mode=True,
    )
    # Init client and result.
    client = lidarr.NamingConfigApi(module.api)
    result = dict(
        changed=False,
    )

    # Get resource.
    result.update(get_naming_config(result).model_dump(by_alias=False))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
