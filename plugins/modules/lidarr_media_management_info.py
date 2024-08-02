#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: lidarr_media_management_info

short_description: Get information about Lidarr media management.

version_added: "1.0.0"

description: Get information about Lidarr media management.

extends_documentation_fragment:
    - devopsarr.lidarr.lidarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# fetch media management
- name: fetch media management info
  devopsarr.lidarr.lidarr_media_management_info:
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Media management ID.
    type: int
    returned: always
    sample: '1'
chmod_folder:
    description: Permission in linux format.
    returned: always
    type: str
    sample: '755'
rescan_after_refresh:
    description: Rescan after refresh.
    returned: always
    type: str
    sample: 'afterManual'
recycle_bin:
    description: Bin path.
    returned: always
    type: str
    sample: '/tmp'
file_date:
    description: File date modification.
    returned: always
    type: str
    sample: 'localAirDate'
extra_file_extensions:
    description: Comma separated list of extra files extension to be imported.
    returned: always
    type: str
    sample: 'srt,info'
download_propers_and_repacks:
    description: Download propers and repack.
    returned: always
    type: str
    sample: 'preferAndUpgrade'
allow_fingerprinting:
    description: Allow fingerprinting.
    returned: always
    type: str
    sample: "always"
chown_group:
    description: Linux group.
    returned: always
    type: str
    sample: 'arrs'
minimum_free_space_when_importing:
    description: Minimum free space when importing.
    returned: always
    type: int
    sample: '100'
recycle_bin_cleanup_days:
    description: Recycle bin days.
    returned: always
    type: int
    sample: '7'
watch_library_for_changes:
    description: Watch library for changes flag.
    returned: always
    type: bool
    sample: false
auto_unmonitor_previously_downloaded_tracks:
    description: Auto unmonitor previously downloaded tracks.
    returned: always
    type: bool
    sample: 'true'
skip_free_space_check_when_importing:
    description: Skip free space check when importing.
    returned: always
    type: bool
    sample: 'true'
set_permissions_linux:
    description: Set linux permission flag.
    returned: always
    type: bool
    sample: 'true'
import_extra_files:
    description: Import extra files flag.
    returned: always
    type: bool
    sample: 'true'
enable_media_info:
    description: Enable media info flag.
    returned: always
    type: bool
    sample: 'true'
delete_empty_folders:
    description: Delete empty folders.
    returned: always
    type: bool
    sample: 'true'
create_empty_artist_folders:
    description: create empty artist folder.
    returned: always
    type: bool
    sample: 'true'
copy_using_hardlinks:
    description: Copy using hardlinks.
    returned: always
    type: bool
    sample: 'true'
auto_rename_folders:
    description: Auto rename folders.
    returned: always
    type: bool
    sample: 'true'
paths_default_static:
    description: Paths default static.
    returned: always
    type: bool
    sample: 'true'
'''

from ansible_collections.devopsarr.lidarr.plugins.module_utils.lidarr_module import LidarrModule
from ansible.module_utils.common.text.converters import to_native

try:
    import lidarr
    HAS_LIDARR_LIBRARY = True
except ImportError:
    HAS_LIDARR_LIBRARY = False


def get_media_management_config(result):
    try:
        return client.get_media_management_config()
    except lidarr.ApiException as e:
        module.fail_json('Error getting media management: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error getting media management: {}'.format(to_native(e)), **result)


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = LidarrModule(
        argument_spec={},
        supports_check_mode=True,
    )
    # Init client and result.
    client = lidarr.MediaManagementConfigApi(module.api)
    result = dict(
        changed=False,
    )

    # Get resource.
    result.update(get_media_management_config(result).model_dump(by_alias=False))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
