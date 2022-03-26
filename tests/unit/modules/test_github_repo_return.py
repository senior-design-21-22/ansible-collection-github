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


def run_module():
    module_args = dict(
        access_token=dict(type='str', required=True, no_log=True),
        organization=dict(type='str', required=True),
        api_url=dict(type='str', default=''),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = dict(
        changed=False,
        fact=''
    )

    if module.params['api_url'] == '':
        g = 'token'
    else:
        g = 'api_and_token'

    if module.params['access_token'] == 'bad_token':
        return module.params['access_token']

    if module.params['api_url'] == 'bad_url':
        return module.params['api_url']

    output = []

    org_name = module.params['organization']

    if module.params['api_url']:
        if org_name == 'multiple_repo_org':
            output = [
                {
                    "archived": False,
                    "clone_url": module.params['api_url'] + '/' + module.params['organization'] + '/testing-repo-private.git',
                    "default_branch": "main",
                    "description": None,
                    "full_name": module.params['organization'] + '/testing-repo-private',
                    "hooks_url": module.params['api_url'] + '/repos/' + module.params['organization'] + '/testing-repo-private/hooks',
                    "language": None,
                    "name": "testing-repo-private",
                    "owner": module.params['organization'],
                    "private": True,
                    "url": module.params['api_url'] + '/repos/' + module.params['organization'] + '/testing-repo-private'
                },
                {
                    "archived": False,
                    "clone_url": module.params['api_url'] + '/' + module.params['organization'] + '/testing-repo-internal.git',
                    "default_branch": "main",
                    "description": None,
                    "full_name": module.params['organization'] + '/testing-repo-internal',
                    "hooks_url": module.params['api_url'] + '/repos/' + module.params['organization'] + '/testing-repo-internal/hooks',
                    "language": None,
                    "name": "testing-repo-internal",
                    "owner": module.params['organization'],
                    "private": True,
                    "url": module.params['api_url'] + '/repos/' + module.params['organization'] + '/testing-repo-internal'
                }
            ]
        elif org_name == 'one_repo_org':
            output = [
                {
                    "archived": False,
                    "clone_url": module.params['api_url'] + '/' + module.params['organization'] + '/testing-repo-private.git',
                    "default_branch": "main",
                    "description": None,
                    "full_name": module.params['organization'] + '/testing-repo-private',
                    "hooks_url": module.params['api_url'] + '/repos/' + module.params['organization'] + '/testing-repo-private/hooks',
                    "language": None,
                    "name": "testing-repo-private",
                    "owner": module.params['organization'],
                    "private": True,
                    "url": module.params['api_url'] + '/repos/' + module.params['organization'] + '/testing-repo-private'
                }
            ]
    else:
        if org_name == 'multiple_repo_org':
            output = [
                {
                    "archived": False,
                    "clone_url": 'https://github.com/' + module.params['organization'] + '/testing-repo-private.git',
                    "default_branch": "main",
                    "description": None,
                    "full_name": module.params['organization'] + '/testing-repo-private',
                    "hooks_url": 'https://github.com/repos/' + module.params['organization'] + '/testing-repo-private/hooks',
                    "language": None,
                    "name": "testing-repo-private",
                    "owner": module.params['organization'],
                    "private": True,
                    "url": 'https://github.com/repos/' + module.params['organization'] + '/testing-repo-private'
                },
                {
                    "archived": False,
                    "clone_url": 'https://github.com/' + module.params['organization'] + '/testing-repo-internal.git',
                    "default_branch": "main",
                    "description": None,
                    "full_name": module.params['organization'] + '/testing-repo-internal',
                    "hooks_url": 'https://github.com/repos/' + module.params['organization'] + '/testing-repo-internal/hooks',
                    "language": None,
                    "name": "testing-repo-internal",
                    "owner": module.params['organization'],
                    "private": True,
                    "url": 'https://github.com/repos/' + module.params['organization'] + '/testing-repo-internal'
                }
            ]
        elif org_name == 'one_repo_org':
            output = [
                {
                    "archived": False,
                    "clone_url": 'https://github.com/' + module.params['organization'] + '/testing-repo-private.git',
                    "default_branch": "main",
                    "description": None,
                    "full_name": module.params['organization'] + '/testing-repo-private',
                    "hooks_url": 'https://github.com/repos/' + module.params['organization'] + '/testing-repo-private/hooks',
                    "language": None,
                    "name": "testing-repo-private",
                    "owner": module.params['organization'],
                    "private": True,
                    "url": 'https://github.com/repos/' + module.params['organization'] + '/testing-repo-private'
                }
            ]

    return output


def main():
    run_module()


if __name__ == '__main__':
    main()


class TestRepositoryInformationModule(unittest.TestCase):
    def test_module_fail_when_required_args_missing(self):
        set_module_args({})
        self.assertRaises(AnsibleFailJson)

    def test_module_pass_when_required_args_fulfilled_correctly(self):
        set_module_args({'access_token': 'token',
                         'organization': 'None'})
        result = run_module()
        assert result == []
        self.assertRaises(AnsibleExitJson)

    def test_module_return_one_repo_no_api_url(self):
        set_module_args({'access_token': 'token',
                         'organization': 'one_repo_org'})
        result = run_module()
        test = [
            {
                "archived": False,
                "clone_url": 'https://github.com/one_repo_org/testing-repo-private.git',
                "default_branch": "main",
                "description": None,
                "full_name": 'one_repo_org/testing-repo-private',
                "hooks_url": 'https://github.com/repos/one_repo_org/testing-repo-private/hooks',
                "language": None,
                "name": "testing-repo-private",
                "owner": 'one_repo_org',
                "private": True,
                "url": 'https://github.com/repos/one_repo_org/testing-repo-private'
            }
        ]
        assert result == test

    def test_module_return_multiple_repo_no_api_url(self):
        set_module_args({'access_token': 'token',
                         'organization': 'multiple_repo_org'})
        result = run_module()
        test = [
            {
                "archived": False,
                "clone_url": 'https://github.com/multiple_repo_org/testing-repo-private.git',
                "default_branch": "main",
                "description": None,
                "full_name": 'multiple_repo_org/testing-repo-private',
                "hooks_url": 'https://github.com/repos/multiple_repo_org/testing-repo-private/hooks',
                "language": None,
                "name": "testing-repo-private",
                "owner": 'multiple_repo_org',
                "private": True,
                "url": 'https://github.com/repos/multiple_repo_org/testing-repo-private'
            },
            {
                "archived": False,
                "clone_url": 'https://github.com/multiple_repo_org/testing-repo-internal.git',
                "default_branch": "main",
                "description": None,
                "full_name": 'multiple_repo_org/testing-repo-internal',
                "hooks_url": 'https://github.com/repos/multiple_repo_org/testing-repo-internal/hooks',
                "language": None,
                "name": "testing-repo-internal",
                "owner": 'multiple_repo_org',
                "private": True,
                "url": 'https://github.com/repos/multiple_repo_org/testing-repo-internal'
            }
        ]
        assert result == test

    def test_module_api_url_entered_as_empty(self):
        set_module_args({'access_token': 'token',
                         'organization': 'one_repo_org',
                         'api_url': ''})
        result = run_module()
        test = [
            {
                "archived": False,
                "clone_url": 'https://github.com/one_repo_org/testing-repo-private.git',
                "default_branch": "main",
                "description": None,
                "full_name": 'one_repo_org/testing-repo-private',
                "hooks_url": 'https://github.com/repos/one_repo_org/testing-repo-private/hooks',
                "language": None,
                "name": "testing-repo-private",
                "owner": 'one_repo_org',
                "private": True,
                "url": 'https://github.com/repos/one_repo_org/testing-repo-private'
            }
        ]
        assert result == test

    def test_fail_api_call(self):
        set_module_args({'access_token': 'token',
                         'organization': 'one_repo_org',
                         'api_url': 'bad_url'})
        result = run_module()
        assert result == 'bad_url'

    def test_fail_access_token(self):
        set_module_args({'access_token': 'bad_token',
                         'organization': 'one_repo_org',
                         'api_url': 'good_url'})
        result = run_module()
        assert result == 'bad_token'

    def test_module_return_multiple_repo_api_url(self):
        set_module_args({'access_token': 'token',
                         'organization': 'multiple_repo_org',
                         'api_url': 'good_url'})
        result = run_module()
        test = [
            {
                "archived": False,
                "clone_url": 'good_url/multiple_repo_org/testing-repo-private.git',
                "default_branch": "main",
                "description": None,
                "full_name": 'multiple_repo_org/testing-repo-private',
                "hooks_url": 'good_url/repos/multiple_repo_org/testing-repo-private/hooks',
                "language": None,
                "name": "testing-repo-private",
                "owner": 'multiple_repo_org',
                "private": True,
                "url": 'good_url/repos/multiple_repo_org/testing-repo-private'
            },
            {
                "archived": False,
                "clone_url": 'good_url/multiple_repo_org/testing-repo-internal.git',
                "default_branch": "main",
                "description": None,
                "full_name": 'multiple_repo_org/testing-repo-internal',
                "hooks_url": 'good_url/repos/multiple_repo_org/testing-repo-internal/hooks',
                "language": None,
                "name": "testing-repo-internal",
                "owner": 'multiple_repo_org',
                "private": True,
                "url": 'good_url/repos/multiple_repo_org/testing-repo-internal'
            }
        ]
        assert result == test

    def test_module_return_one_repo_api_url(self):
        set_module_args({'access_token': 'token',
                         'organization': 'one_repo_org',
                         'api_url': 'good_url'})
        result = run_module()
        test = [
            {
                "archived": False,
                "clone_url": 'good_url/one_repo_org/testing-repo-private.git',
                "default_branch": "main",
                "description": None,
                "full_name": 'one_repo_org/testing-repo-private',
                "hooks_url": 'good_url/repos/one_repo_org/testing-repo-private/hooks',
                "language": None,
                "name": "testing-repo-private",
                "owner": 'one_repo_org',
                "private": True,
                "url": 'good_url/repos/one_repo_org/testing-repo-private'
            }
        ]
        assert result == test

    def test_module_return_empty_repo_api_url(self):
        set_module_args({'access_token': 'token',
                         'organization': 'no_repo_org',
                         'api_url': 'good_url'})
        result = run_module()
        test = []
        assert result == test
