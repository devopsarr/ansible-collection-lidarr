#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: lidarr_tag

short_description: Manages Lidarr tag.

version_added: "1.0.0"

description: Manages Lidarr tag.

options:
    label:
        description: Actual tag.
        required: true
        type: str
    state:
        description: Create or delete a tag.
        required: false
        default: 'present'
        choices: [ "present", "absent" ]
        type: str

extends_documentation_fragment:
    - devopsarr.lidarr.lidarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
# Create a tag
- name: Create a tag
  devopsarr.lidarr.tag:
    label: default

# Delete a tag
- name: Delete a tag
  devopsarr.lidarr.tag:
    label: wrong
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Tag ID.
    type: int
    returned: always
    sample: '1'
label:
    description: The output message that the test module generates.
    type: str
    returned: 'on create/update'
    sample: 'hd'
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.devopsarr.lidarr.plugins.module_utils.lidarr_module import LidarrModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        # TODO: add validation for lowercase tags
        label=dict(type='str', required=True),
        state=dict(default='present', type='str', choices=['present', 'absent']),
    )

    result = dict(
        changed=False,
        id=0,
    )

    module = LidarrModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    tags = module.api.get_tag()

    for tag in tags:
        if tag['label'] == module.params['label']:
            result.update(tag)

    # TODO: add error handling
    if module.params['state'] == 'present' and result['id'] == 0:
        result['changed'] = True
        if not module.check_mode:
            response = module.api.create_tag(module.params['label'])
            result.update(response)
    elif module.params['state'] == 'absent' and result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            response = module.api.del_tag(result['id'])
            result['id'] = 0
    elif module.check_mode:
        module.exit_json(**result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
