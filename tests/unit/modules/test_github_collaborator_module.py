from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils import basic
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_bytes
import unittest
import json


def set_module_args(args):
    if '_ansible_remote_tmp' not in args:
        args['_ansible_remote_tmp'] = '/tmp'
    if '_ansible_keep_remote_files' not in args:
        args['_ansible_keep_remote_files'] = False

    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)


class AnsibleExitJson(Exception):
    pass


class AnsibleFailJson(Exception):
    pass


def exit_json(*args, **kwargs):
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)


def present_collaborator(g, repo, collaborator, permission):
    output = g.copy()
    collaborator_position = next((i for i, x in enumerate(output) if x["login"] == collaborator), None)
    permissions = {}

    if collaborator_position is not None:
        for user in output:
            if collaborator == user['login']:
                if permission == 'admin':
                    permissions = {
                        'admin': True,
                        'pull': True,
                        'push': True,
                        'triage': True
                    }
                elif permission == 'pull':
                    permissions = {
                        'admin': False,
                        'pull': True,
                        'push': True,
                        'triage': True
                    }
                else:
                    permissions = {
                        'admin': False,
                        'pull': False,
                        'push': True,
                        'triage': True
                    }
                user['permissions'] = permissions
                if permission == 'admin':
                    user['site_admin'] = True
                break
    else:
        if permission == 'admin':
            permissions = {
                'admin': True,
                'pull': True,
                'push': True,
                'triage': True
            }
        elif permission == 'pull':
            permissions = {
                'admin': False,
                'pull': True,
                'push': True,
                'triage': True
            }
        else:
            permissions = {
                'admin': False,
                'pull': False,
                'push': True,
                'triage': True
            }
        new_collaborator = {
            'login': collaborator,
            'id': 000,
            'type': 'user',
            'site_admin': False,
            'permissions': permissions
        }
        if permission == 'admin':
            new_collaborator['site_admin'] = True

        output.append(new_collaborator)

    return output


def absent_collaborator(g, repo, collaborator):
    output = g.copy()
    collaborator_position = next((i for i, x in enumerate(output) if x["login"] == collaborator), None)
    if collaborator_position is not None:
        output.pop(collaborator_position)

    print(output)
    return output


def get_collaborators(g, repo):
    collaborator_list = list()

    if repo == 'org/one_collaborator':
        collaborator = {
            'login': 'username',
            'id': 000,
            'type': 'user',
            'site_admin': False,
            'permissions': {
                'triage': True,
                'push': True,
                'pull': False,
                'admin': False
            }
        }
        collaborator_list.append(collaborator)
    elif repo == 'org/multi_collaborator':
        collaborator1 = {
            'login': 'username1',
            'id': 000,
            'type': 'user',
            'site_admin': False,
            'permissions': {
                'triage': True,
                'push': True,
                'pull': False,
                'admin': False
            }
        }
        collaborator2 = {
            'login': 'username2',
            'id': 1,
            'type': 'user',
            'site_admin': False,
            'permissions': {
                'triage': True,
                'push': True,
                'pull': True,
                'admin': False
            }
        }
        collaborator_list.append(collaborator1)
        collaborator_list.append(collaborator2)

    return collaborator_list


def present_collaborator_check_mode(g, repo, collaborator, permission, current_collaborators):
    collaborator_position = next((i for i, x in enumerate(current_collaborators) if x["login"] == collaborator), None)
    permissions = {}
    if permission == 'admin':
        permissions = {
            'admin': True,
            'pull': True,
            'push': True,
            'triage': True
        }
    elif permission == 'pull':
        permissions = {
            'admin': False,
            'pull': True,
            'push': True,
            'triage': True
        }
    else:
        permissions = {
            'admin': False,
            'pull': False,
            'push': True,
            'triage': True
        }

    output_collaborators = current_collaborators.copy()
    if collaborator_position is None:

        collaborator_to_add = {
            'login': collaborator,
            'id': 000,
            'type': 'User',
            'site_admin': True if permission == 'admin' else False,
            'permissions': permissions
        }
        output_collaborators.append(collaborator_to_add)

    else:
        for current_collaborator in output_collaborators:
            if collaborator == current_collaborator['login']:
                current_collaborator['permissions'] = permissions
                if permission == 'admin':
                    current_collaborator['site_admin'] = True

    return output_collaborators


def absent_collaborator_check_mode(g, repo, collaborator, current_collaborators):
    collaborator_position = next((i for i, x in enumerate(current_collaborators) if x["login"] == collaborator), None)
    output_collaborators = current_collaborators.copy()
    if collaborator_position is not None:
        output_collaborators.remove(collaborator_position)

    return output_collaborators


def run_module():
    module_args = dict(
        access_token=dict(type='str', default='No Token Provided'),
        organization=dict(type='str', default='default'),
        api_url=dict(type='str', default=''),
        repository=dict(type='str', default=''),
        collaborator=dict(type='str', default=''),
        permission=dict(type='str', default=''),
        state=dict(type='str', default='present'),
        check_mode=dict(type='bool', default=False)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = dict(
        changed=False,
        fact=''
    )

    valid_permissions = ["push", "pull", "admin"]

    changed = False

    if(module.params['api_url'] == ''):
        g = module.params['access_token']
    else:
        g = module.params['access_token'] + module.params['api_url']

    if len(module.params['repository']):
        module.params['repository'] = module.params['organization'] + \
            "/" + module.params['repository']

    current_collaborators = get_collaborators(g, module.params['repository'])

    output = []

    if module.params['state'] == 'present':
        if len(module.params['collaborator']) and len(module.params['repository']) and module.params['permission'].lower() in valid_permissions:
            if module.check_mode is False:
                output = present_collaborator(current_collaborators, module.params['repository'], module.params['collaborator'], module.params['permission'])
            else:
                output = present_collaborator_check_mode(g, module.params['repository'],
                                                         module.params['collaborator'], module.params['permission'], current_collaborators)
        elif module.params['permission'].lower() not in valid_permissions:
            error_message = 'Permissions must be \'push\' \'pull\' or \'admin\''
            return error_message, changed

    if module.params['state'] == 'absent' and len(module.params['repository']):
        if module.check_mode is False:
            output = absent_collaborator(current_collaborators, module.params['repository'], module.params['collaborator'])
        else:
            output = absent_collaborator_check_mode(g, module.params['repository'], module.params['collaborator'], current_collaborators)

    current_collaborators = get_collaborators(g, module.params['repository'])

    if current_collaborators != output:
        changed = True

    return output, changed


class TestCollaboratorModule(unittest.TestCase):
    def test_module_passing_valid_arguments(self):
        set_module_args({'access_token': 'token',
                         'organization': 'org',
                         'repository': 'one_collaborator',
                         'collaborator': 'username',
                         'permission': 'push',
                         'state': 'present'})
        self.assertRaises(AnsibleExitJson)

    def test_module_returning_collaborator_already_there(self):
        set_module_args({'access_token': 'token',
                         'organization': 'org',
                         'repository': 'one_collaborator',
                         'collaborator': 'username',
                         'permission': 'push',
                         'state': 'present'})

        result, changed = run_module()

        test = [{
            'login': 'username',
            'id': 0,
            'type': 'user',
            'site_admin': False,
            'permissions': {
                'triage': True,
                'push': True,
                'pull': False,
                'admin': False
            }
        }]

        assert result == test
        assert changed is False

    def test_module_adding_collaborator_to_empty_list(self):
        set_module_args({'access_token': 'token',
                         'organization': 'org',
                         'repository': 'no_collaborator',
                         'collaborator': 'new_username',
                         'permission': 'push',
                         'state': 'present'})

        result, changed = run_module()

        test = [{
            'login': 'new_username',
            'id': 0,
            'type': 'user',
            'site_admin': False,
            'permissions': {
                'triage': True,
                'push': True,
                'pull': False,
                'admin': False
            }
        }]

        assert result == test
        assert changed is True

    def test_module_adding_collaborator_to_populated_list(self):
        set_module_args({'access_token': 'token',
                         'organization': 'org',
                         'repository': 'one_collaborator',
                         'collaborator': 'new_username',
                         'permission': 'push',
                         'state': 'present'})

        result, changed = run_module()

        test = [{
            'login': 'username',
            'id': 0,
            'type': 'user',
            'site_admin': False,
            'permissions': {
                'triage': True,
                'push': True,
                'pull': False,
                'admin': False
            }
        },
            {
                'login': 'new_username',
                'id': 0,
                'type': 'user',
                'site_admin': False,
                'permissions': {
                    'triage': True,
                    'push': True,
                    'pull': False,
                    'admin': False
                }
        }]

        assert result == test
        assert changed is True

    def test_module_changing_collaborator_permissions(self):
        set_module_args({'access_token': 'token',
                         'organization': 'org',
                         'repository': 'one_collaborator',
                         'collaborator': 'username',
                         'permission': 'admin',
                         'state': 'present'})

        result, changed = run_module()

        test = [{
            'login': 'username',
            'id': 0,
            'type': 'user',
            'site_admin': True,
            'permissions': {
                'triage': True,
                'push': True,
                'pull': True,
                'admin': True
            }
        }]

        assert result == test
        assert changed is True

    def test_module_remove_collaborator_from_empty_list(self):
        set_module_args({'access_token': 'token',
                         'organization': 'org',
                         'repository': 'no_collaborator',
                         'collaborator': 'username',
                         'permission': 'admin',
                         'state': 'absent'})

        result, changed = run_module()

        test = []

        assert result == test
        assert changed is False

    def test_module_remove_collaborator_from_populated_list(self):
        set_module_args({'access_token': 'token',
                         'organization': 'org',
                         'repository': 'one_collaborator',
                         'collaborator': 'username',
                         'permission': 'admin',
                         'state': 'absent'})

        result, changed = run_module()

        test = []

        assert result == test
        assert changed is True

    def test_module_incorrect_permission(self):
        set_module_args({'access_token': 'token',
                         'organization': 'org',
                         'repository': 'one_collaborator',
                         'collaborator': 'username',
                         'permission': 'Not a real permission',
                         'state': 'present'})

        result, changed = run_module()

        test = 'Permissions must be \'push\' \'pull\' or \'admin\''

        assert result == test
        assert changed is False

    def test_module_check_mode_adding_collaborator(self):
        set_module_args({'access_token': 'token',
                         'organization': 'org',
                         'repository': 'one_collaborator',
                         'collaborator': 'username',
                         'permission': 'push',
                         'state': 'present',
                         'check_mode': True})

        result, changed = run_module()

        test = [{
            'login': 'username',
            'id': 0,
            'type': 'user',
            'site_admin': False,
            'permissions': {
                'triage': True,
                'push': True,
                'pull': False,
                'admin': False
            }
        }]

        assert result == test
        assert changed is False

    def test_module_check_mode_adding_collaborator_to_empty_list(self):
        set_module_args({'access_token': 'token',
                         'organization': 'org',
                         'repository': 'no_collaborator',
                         'collaborator': 'new_username',
                         'permission': 'push',
                         'state': 'present',
                         'check_mode': True})

        result, changed = run_module()

        test = [{
            'login': 'new_username',
            'id': 0,
            'type': 'user',
            'site_admin': False,
            'permissions': {
                'triage': True,
                'push': True,
                'pull': False,
                'admin': False
            }
        }]

        assert result == test
        assert changed is True

    def test_module_check_mode_adding_collaborator_to_populated_list(self):
        set_module_args({'access_token': 'token',
                         'organization': 'org',
                         'repository': 'one_collaborator',
                         'collaborator': 'new_username',
                         'permission': 'push',
                         'state': 'present',
                         'check_mode': True})

        result, changed = run_module()

        test = [{
            'login': 'username',
            'id': 0,
            'type': 'user',
            'site_admin': False,
            'permissions': {
                'triage': True,
                'push': True,
                'pull': False,
                'admin': False
            }
        },
            {
                'login': 'new_username',
                'id': 0,
                'type': 'user',
                'site_admin': False,
                'permissions': {
                    'triage': True,
                    'push': True,
                    'pull': False,
                    'admin': False
                }
        }]

        assert result == test
        assert changed is True

    def test_module_check_mode_changing_collaborator_permissions(self):
        set_module_args({'access_token': 'token',
                         'organization': 'org',
                         'repository': 'one_collaborator',
                         'collaborator': 'username',
                         'permission': 'admin',
                         'state': 'present',
                         'check_mode': True})

        result, changed = run_module()

        test = [{
            'login': 'username',
            'id': 0,
            'type': 'user',
            'site_admin': True,
            'permissions': {
                'triage': True,
                'push': True,
                'pull': True,
                'admin': True
            }
        }]

        assert result == test
        assert changed is True

    def test_module_check_mode_remove_collaborator_from_empty_list(self):
        set_module_args({'access_token': 'token',
                         'organization': 'org',
                         'repository': 'no_collaborator',
                         'collaborator': 'username',
                         'permission': 'admin',
                         'state': 'absent',
                         'check_mode': True})

        result, changed = run_module()

        test = []

        assert result == test
        assert changed is False

    def test_module_check_mode_remove_collaborator_from_populated_list(self):
        set_module_args({'access_token': 'token',
                         'organization': 'org',
                         'repository': 'one_collaborator',
                         'collaborator': 'username',
                         'permission': 'admin',
                         'state': 'absent',
                         'check_mode': True})

        result, changed = run_module()

        test = []

        assert result == test
        assert changed is True
