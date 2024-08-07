#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: lidarr_download_client_config

short_description: Manages Lidarr download client config.

version_added: "1.0.0"

description: Manages Lidarr download client config.

options:
    auto_redownload_failed:
        description: Auto redownload failed.
        required: true
        type: bool
    auto_redownload_failed_from_interactive_search:
        description: Auto redownload failed from interactive search.
        required: true
        type: bool
    enable_completed_download_handling:
        description: Enable completed download handling.
        required: true
        type: bool

extends_documentation_fragment:
    - devopsarr.lidarr.lidarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# update download client config
- name: Update download client config
  devopsarr.lidarr.lidarr_download_client_config:
    auto_redownload_failed: false
    auto_redownload_failed_from_interactive_search: false
    enable_completed_download_handling: true
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
auto_redownload_failed_from_interactive_search:
    description: Auto redownload failed from interactive search.
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


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        enable_completed_download_handling=dict(type='bool', required=True),
        auto_redownload_failed_from_interactive_search=dict(type='bool', required=True),
        auto_redownload_failed=dict(type='bool', required=True),
    )


def read_download_client_config(result):
    try:
        return client.get_download_client_config()
    except lidarr.ApiException as e:
        module.fail_json('Error getting download client config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error getting download client config: {}'.format(to_native(e)), **result)


def update_download_client_config(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.update_download_client_config(download_client_config_resource=want, id="1")
        except lidarr.ApiException as e:
            module.fail_json('Error updating download client config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating download client config: {}'.format(to_native(e)), **result)
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
    client = lidarr.DownloadClientConfigApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Get resource.
    state = read_download_client_config(result)
    if state:
        result.update(state.model_dump(by_alias=False))

    want = lidarr.DownloadClientConfigResource(
        enable_completed_download_handling=module.params['enable_completed_download_handling'],
        auto_redownload_failed=module.params['auto_redownload_failed'],
        auto_redownload_failed_from_interactive_search=module.params['auto_redownload_failed_from_interactive_search'],
        download_client_working_folders='_UNPACK_|_FAILED_',
        id=1,
    )

    # Update an existing resource.
    if want != state:
        update_download_client_config(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
