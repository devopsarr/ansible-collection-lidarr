#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: lidarr_artist

short_description: Manages lidarr Artist.

version_added: "1.0.0"

description: Manages lidarr Artist.

options:
    monitored:
        description: Monitored flag.
        type: bool
        default: false
    quality_profile_id:
        description: Quality profile ID.
        type: int
    metadata_profile_id:
        description: Metadata profile ID.
        type: int
    foreign_artist_id:
        description: Foreign artist ID.
        required: true
        type: str
    path:
        description: Artist path.
        required: true
        type: str
    artist_name:
        description: Artist name.
        required: true
        type: str

extends_documentation_fragment:
    - devopsarr.lidarr.lidarr_credentials
    - devopsarr.lidarr.lidarr_taggable
    - devopsarr.lidarr.lidarr_state

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a artist
- name: Create a artist
  devopsarr.lidarr.lidarr_artist:
    artist_name: "Queen"
    foreign_artist_id: "0383dadf-2a4e-4d10-a46a-e9e041da8eb3"
    monitored: true
    path: "/config/queen"
    quality_profile_id: 1
    metadata_profile_id: 1
    tags: [1,2]

# Delete a artist
- name: Delete a artist
  devopsarr.lidarr.lidarr_artist:
    artist_name: "Queen"
    foreign_artist_id: "0383dadf-2a4e-4d10-a46a-e9e041da8eb3"
    path: "/config/queen"
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
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
    HAS_lidarr_LIBRARY = True
except ImportError:
    HAS_lidarr_LIBRARY = False


def is_changed(status, want):
    if (want.artist_name != status.artist_name or
            want.monitored != status.monitored or
            want.quality_profile_id != status.quality_profile_id or
            want.metadata_profile_id != status.metadata_profile_id or
            want.foreign_artist_id != status.foreign_artist_id or
            want.path != status.path or
            want.tags != status.tags):
        return True

    return False


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        monitored=dict(type='bool', default=False),
        artist_name=dict(type='str', required=True),
        path=dict(type='str', required=True),
        quality_profile_id=dict(type='int'),
        metadata_profile_id=dict(type='int'),
        foreign_artist_id=dict(type='str', required=True),
        tags=dict(type='list', elements='int', default=[]),
        state=dict(default='present', type='str', choices=['present', 'absent']),
    )


def create_artist(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.create_artist(artist_resource=want)
        except lidarr.ApiException as e:
            module.fail_json('Error creating artist: {}\n body {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error creating artist: {}'.format(to_native(e)), **result)
        result.update(response.model_dump(by_alias=False))
    module.exit_json(**result)


def list_artist(result):
    try:
        return client.list_artist()
    except lidarr.ApiException as e:
        module.fail_json('Error listing artist: {}\n body {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing artist: {}'.format(to_native(e)), **result)


def find_artist(foreign_artist_id, result):
    for artist in list_artist(result):
        if artist.foreign_artist_id == foreign_artist_id:
            return artist
    return None


def update_artist(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.update_artist(artist_resource=want, id=str(want.id))
        except lidarr.ApiException as e:
            module.fail_json('Error updating artist: {}\n body {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating artist: {}'.format(to_native(e)), **result)
    # No need to exit module since it will exit by default either way
    result.update(response.model_dump(by_alias=False))


def delete_artist(result):
    if result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            try:
                client.delete_artist(result['id'])
            except lidarr.ApiException as e:
                module.fail_json('Error deleting artist: {}\n body {}'.format(to_native(e.reason), to_native(e.body)), **result)
            except Exception as e:
                module.fail_json('Error deleting artist: {}'.format(to_native(e)), **result)
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
    client = lidarr.ArtistApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Check if a resource is present already.
    state = find_artist(module.params['foreign_artist_id'], result)
    if state:
        result.update(state.model_dump(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        delete_artist(result)

    # Set wanted resource.
    want = lidarr.ArtistResource(
        artist_name=module.params['artist_name'],
        monitored=module.params['monitored'],
        quality_profile_id=module.params['quality_profile_id'],
        metadata_profile_id=module.params['metadata_profile_id'],
        foreign_artist_id=module.params['foreign_artist_id'],
        path=module.params['path'],
        tags=module.params['tags'],
        add_options=lidarr.AddArtistOptions(
            monitor='all',
        ),
    )

    # Create a new resource if needed.
    if result['id'] == 0:
        create_artist(want, result)

    # Update an existing resource.
    want.id = result['id']
    if is_changed(state, want):
        update_artist(want, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
