#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

DOCUMENTATION = r'''
---
module: lidarr_system_info

short_description: Lidarr system info module

version_added: "0.0.1"

description: Provide Lidarr system info

extends_documentation_fragment:
    - devopsarr.lidarr.lidarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
# It will fetch the system info
- name: Get system info
  devopsarr.lidarr.lidarr_system_info:
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
app_name:
    description: It should be Lidarr.
    type: str
    returned: always
    sample: 'Lidarr'
version:
    description: Binary version.
    type: str
    returned: always
    sample: '3.0.8.1507'
build_time:
    description: Build time.
    type: str
    returned: always
    sample: '2022-04-23T21:40:53Z'
is_debug:
    description: Debug flag.
    type: bool
    returned: always
    sample: 'false'
is_production:
    description: Production flag.
    type: bool
    returned: always
    sample: 'false'
is_admin:
    description: Admin flag.
    type: bool
    returned: always
    sample: 'false'
is_user_interactive:
    description: User interactive flag.
    type: bool
    returned: always
    sample: 'false'
startup_path:
    description: Startup path.
    type: str
    returned: always
    sample: '/app/lidarr/bin'
app_data:
    description: Configuration path.
    type: str
    returned: always
    sample: '/config'
os_name:
    description: Host OS.
    type: str
    returned: always
    sample: 'ubuntu'
os_version:
    description: Host OS version.
    type: str
    returned: always
    sample: '20.04'
is_mono_runtime:
    description: Mono runtime flag.
    type: bool
    returned: always
    sample: 'true'
is_mono:
    description: Mono flag.
    type: bool
    returned: always
    sample: 'true'
is_linux:
    description: Linux flag.
    type: bool
    returned: always
    sample: 'false'
is_osx:
    description: OSX flag.
    type: bool
    returned: always
    sample: 'false'
is_windows:
    description: Windows flag.
    type: str
    returned: always
    sample: 'false'
mode:
    description: Mode.
    type: str
    returned: always
    sample: 'console'
branch:
    description: Lidarr branch.
    type: str
    returned: always
    sample: 'master'
authentication:
    description: Authentication type.
    type: str
    returned: always
    sample: 'none'
sqlite_version:
    description: SQLite version.
    type: str
    returned: always
    sample: '3.31.1'
url_base:
    description: URI prefix for installation.
    type: str
    returned: always
    sample: '/lidarr'
runtime_version:
    description: Runtime version.
    type: str
    returned: always
    sample: '6.12.0.122'
runtime_name:
    description: Runtime name.
    type: str
    returned: always
    sample: 'mono'
start_time:
    description: Start time.
    type: str
    returned: always
    sample: '2022-06-09T08:21:23.970798Z'
package_version:
    description: Package version.
    type: str
    returned: always
    sample: '3.0.8.1507-ls148'
package_author:
    description: Package author.
    type: str
    returned: always
    sample: '[linuxserver.io](https://linuxserver.io)'
package_update_mechanism:
    description: Package update mechanism.
    type: str
    returned: always
    sample: 'docker'
'''

from ansible_collections.devopsarr.lidarr.plugins.module_utils.lidarr_module import LidarrModule
from ansible.module_utils.common.text.converters import to_native

try:
    import lidarr
    HAS_LIDARR_LIBRARY = True
except ImportError:
    HAS_LIDARR_LIBRARY = False

__metaclass__ = type


def get_system_status(result):
    try:
        return client.get_system_status()
    except lidarr.ApiException as e:
        module.fail_json('Error retrieving system status: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error retrieving system status: {}'.format(to_native(e)), **result)


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = LidarrModule(
        argument_spec={},
        supports_check_mode=True,
    )
    # Init client and result.
    client = lidarr.SystemApi(module.api)
    result = dict(
        changed=False,
    )

    # Get resources.
    result.update(get_system_status(result).model_dump(by_alias=False))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
