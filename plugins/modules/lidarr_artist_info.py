#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: lidarr_artist_info

short_description: Get information about Lidarr artist.

version_added: "1.0.0"

description: Get information about Lidarr artist.

options:
    foreign_artist_id:
        description: Foreign artist ID.
        type: str

extends_documentation_fragment:
    - devopsarr.lidarr.lidarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Gather information about all artist.
- name: Gather information about all artist
  devopsarr.lidarr.lidarr_artist_info:

# Gather information about a single artist.
- name: Gather information about a single artist
  devopsarr.lidarr.lidarr_artist_info:
    foreign_artist_id: "0383dadf-2a4e-4d10-a46a-e9e041da8eb3"
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
artist_list:
    description: A list of artist.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: artist ID.
            type: int
            returned: always
            sample: 1
        monitored:
            description: Monitored flag.
            type: bool
            returned: always
            sample: false
        quality_profile_id:
            description: Quality profile ID.
            type: int
            returned: always
            sample: 1
        metadata_profile_id:
            description: Metadata profile ID.
            type: int
            returned: always
            sample: 1
        foreign_artist_id:
            description: Foreign artist ID.
            type: str
            returned: always
            sample: "0383dadf-2a4e-4d10-a46a-e9e041da8eb3"
        path:
            description: Artist path.
            type: str
            returned: always
            sample: "/artist/artist_artist_name"
        artist_name:
            description: Artist name.
            type: str
            returned: always
            sample: "Artist name"
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
        foreign_artist_id=dict(type='str'),
    )


def list_artist(result):
    try:
        return client.list_artist()
    except lidarr.ApiException as e:
        module.fail_json('Error listing artist: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing artist: {}'.format(to_native(e)), **result)


def populate_artist(result):
    artist = []
    # Check if a resource is present already.
    for single_artist in list_artist(result):
        if module.params['foreign_artist_id']:
            if single_artist.foreign_artist_id == module.params['foreign_artist_id']:
                artist = [single_artist.model_dump(by_alias=False)]
        else:
            artist.append(single_artist.model_dump(by_alias=False))
    return artist


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = LidarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = lidarr.ArtistApi(module.api)
    result = dict(
        changed=False,
        artist_list=[],
    )

    # List resources.
    result.update(artist_list=populate_artist(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
