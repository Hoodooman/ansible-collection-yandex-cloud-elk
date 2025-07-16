#!/usr/bin/python

# Copyright: (c) 2024, Your Name <your.email@example.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: create_file

short_description: Create a text file with specified content

version_added: "1.0.0"

description: This module creates a text file at the specified path with given content.

options:
    path:
        description: Absolute path where the file should be created
        required: true
        type: str
    content:
        description: Content to write to the file
        required: true
        type: str

author:
    - Your Name (@shvirtd-19)
'''

EXAMPLES = r'''
- name: Create a test file
  my_own_namespace.yandex_cloud_elk.create_file:
    path: /tmp/testfile.txt
    content: "Test ansible module hw 08-ansible-06-module"
'''

RETURN = r'''
file_path:
    description: Path of the created file
    type: str
    returned: always
    sample: '/tmp/testfile.txt'
file_content:
    description: Content written to the file
    type: str
    returned: always
    sample: 'Test ansible module hw 08-ansible-06-module'
'''

from ansible.module_utils.basic import AnsibleModule
import os

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        file_path='',
        file_content=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']
    result['file_path'] = path
    result['file_content'] = content

    if module.check_mode:
        # Check if file would be created or modified
        if not os.path.exists(path):
            result['changed'] = True
        else:
            with open(path, 'r') as f:
                if f.read() != content:
                    result['changed'] = True
        module.exit_json(**result)

    # Main logic
    changed = False
    if os.path.exists(path):
        with open(path, 'r') as f:
            if f.read() != content:
                changed = True
    else:
        changed = True

    if changed:
        try:
            with open(path, 'w') as f:
                f.write(content)
            result['changed'] = True
        except Exception as e:
            module.fail_json(msg=f"Failed to create file: {str(e)}", **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()