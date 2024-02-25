#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: lidarr_download_client_config_info

short_description: Get information about Lidarr download client config.

version_added: "1.0.0"

description: Get information about Lidarr download client config.

extends_documentation_fragment:
    - devopsarr.lidarr.lidarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# fetch download client config
- name: fetch download client config
  devopsarr.lidarr.lidarr_download_client_config_info:
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Download client config ID.
    type: int
    returned: always
    sample: '1'
auto_redownload_failed:
    description: Auto redownload failed.
    returned: always
    type: bool
    sample: true
enable_completed_download_handling:
    description: Enable completed download handling.
    returned: always
    type: bool
    sample: true
download_client_working_folders:
    description: Download client working folders.
    returned: always
    type: str
    sample: '_UNPACK_|_FAILED_'
'''

from ansible_collections.devopsarr.lidarr.plugins.module_utils.lidarr_module import LidarrModule
from ansible.module_utils.common.text.converters import to_native

try:
    import lidarr
    HAS_LIDARR_LIBRARY = True
except ImportError:
    HAS_LIDARR_LIBRARY = False


def get_download_client_config(result):
    try:
        return client.get_download_client_config()
    except Exception as e:
        module.fail_json('Error getting download client config: %s' % to_native(e.reason), **result)


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = LidarrModule(
        argument_spec={},
        supports_check_mode=True,
    )
    # Init client and result.
    client = lidarr.DownloadClientConfigApi(module.api)
    result = dict(
        changed=False,
    )

    # Get resource.
    result.update(get_download_client_config(result).model_dump(by_alias=False))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()