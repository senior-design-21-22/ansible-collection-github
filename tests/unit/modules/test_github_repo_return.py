from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils import basic
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_bytes
import unittest
import json


class Repository:
    def __init__(self):
        self.archived = False
        self.clone_url = 'https://api.github.com/github/Hello-World.git'
        self.default_branch = "main"
        self.description =  ""
        self.full_name = 'github/Hello-World'
        self.hooks_url = 'https://api.github.com/repos/github/Hello-World/hooks'
        self.language = None
        self.name = "Hello-World"
        self.owner = {
            'login': 'github'
        }
        self.private = True
        self.url = "https://api.github.com/orgs/github/repos/Hello-World"
        self.raw_data = {
            'visibility': 'public',
            'is_template': False
        }
    
    def __init__(self, name):
        self.archived = False
        self.clone_url = 'https://api.github.com/github/' + name + '.git'
        self.default_branch = "main"
        self.description =  ""
        self.full_name = 'github/' + name
        self.hooks_url = 'https://api.github.com/github/repos/' + name + '/hooks'
        self.language = None
        self.name = name
        self.owner = {
            'login': 'github'
        }
        self.private = True
        self.url = "https://api.github.com/orgs/github/repos/" + name
        self.raw_data = {
            'visibility': 'public',
            'is_template': False
        }
    

class Organization:
    def __init__(self):
        self.login = "login"
        self.id = 1
        self.node_id = -1
        self.url = "https://api.github.com/orgs/github"
        self.repos_url = "https://api.github.com/orgs/github/repos"
        self.description = "A great organization"
        self.name = "github"
        self.type = "Organization"

    def __init__(self, name):
        self.name = name
        self.login = "login"
        self.id = 1
        self.node_id = -1
        self.url = "https://api.github.com/orgs/" + name
        self.repos_url = "https://api.github.com/orgs/" + name + "/repos"
        self.description = "A great organization"
        self.type = "Organization"

    def get_repos(self):
        repositories = []
        if self.name == 'github':
            repositories = [
                Repository(name='Hello-World'),
                Repository(name='Goodbye-Chat')
            ]

        return repositories


class Github:
    def __init__(self, access_token, base_url=''):
        self.access_token = access_token
        self.base_url = base_url

    def get_organization(self, organization):
        if self.access_token == 'token':
            organization = Organization(name=organization)
        return organization


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
        g = Github(module.params['access_token'])
    else:
        g = Github(module.params['access_token'],
                   base_url=module.params['api_url'])

    output = []

    org_name = module.params['organization']

    for repo in g.get_organization(org_name).get_repos():
        current_repo_dict = {
            "name": repo.name,
            "full_name": repo.full_name,
            "owner": repo.owner['login'],
            "description": repo.description,
            "private": repo.private,
            "archived": repo.archived,
            "language": repo.language,
            "url": repo.url,
            "default_branch": repo.default_branch,
            "hooks_url": repo.hooks_url,
            "clone_url": repo.clone_url
        }
        if len(module.params["api_url"]) == 0:
            current_repo_dict["visibility"] = repo.raw_data["visibility"]
            current_repo_dict["is_template"] = repo.raw_data["is_template"]

        output.append(current_repo_dict)

    # module.exit_json(repos=output)
    return output


class TestRepositoryInformationModule(unittest.TestCase):
    def test_module_fail_when_required_args_missing(self):
        set_module_args({})
        self.assertRaises(AnsibleFailJson)

    def test_module_return_repo(self):
        set_module_args({
            'access_token': 'token',
            'organization': 'github',
            'api_url': ''
        })
        test = [
            {
                "name": 'Hello-World',
                "full_name": 'github/Hello-World',
                "owner": 'github',
                "description": "",
                "private": True,
                "archived": False,
                "language": None,
                "url": "https://api.github.com/orgs/github/repos/Hello-World",
                "default_branch": 'main',
                "hooks_url": 'https://api.github.com/github/repos/Hello-World/hooks',
                "clone_url": 'https://api.github.com/github/Hello-World.git',
                'visibility': 'public',
                'is_template': False
            },
            {
                "name": 'Goodbye-Chat',
                "full_name": 'github/Goodbye-Chat',
                "owner": 'github',
                "description": "",
                "private": True,
                "archived": False,
                "language": None,
                "url": "https://api.github.com/orgs/github/repos/Goodbye-Chat",
                "default_branch": 'main',
                "hooks_url": 'https://api.github.com/github/repos/Goodbye-Chat/hooks',
                "clone_url": 'https://api.github.com/github/Goodbye-Chat.git',
                'visibility': 'public',
                'is_template': False
            }
        ]

        output = run_module()
        print(output)
        assert test == output

    # def test_module_pass_when_required_args_fulfilled_correctly(self):
    #     set_module_args({'access_token': 'token',
    #                      'organization': 'None'})
    #     result = run_module()
    #     assert result == []
    #     self.assertRaises(AnsibleExitJson)

    # def test_module_return_one_repo_no_api_url(self):
    #     set_module_args({'access_token': 'token',
    #                      'organization': 'one_repo_org'})
    #     result = run_module()
    #     test = [
    #         {
    #             "archived": False,
    #             "clone_url": 'https://github.com/one_repo_org/testing-repo-private.git',
    #             "default_branch": "main",
    #             "description": None,
    #             "full_name": 'one_repo_org/testing-repo-private',
    #             "hooks_url": 'https://github.com/repos/one_repo_org/testing-repo-private/hooks',
    #             "language": None,
    #             "name": "testing-repo-private",
    #             "owner": 'one_repo_org',
    #             "private": True,
    #             "url": 'https://github.com/repos/one_repo_org/testing-repo-private'
    #         }
    #     ]
    #     assert result == test

    # def test_module_return_multiple_repo_no_api_url(self):
    #     set_module_args({'access_token': 'token',
    #                      'organization': 'multiple_repo_org'})
    #     result = run_module()
    #     test = [
    #         {
    #             "archived": False,
    #             "clone_url": 'https://github.com/multiple_repo_org/testing-repo-private.git',
    #             "default_branch": "main",
    #             "description": None,
    #             "full_name": 'multiple_repo_org/testing-repo-private',
    #             "hooks_url": 'https://github.com/repos/multiple_repo_org/testing-repo-private/hooks',
    #             "language": None,
    #             "name": "testing-repo-private",
    #             "owner": 'multiple_repo_org',
    #             "private": True,
    #             "url": 'https://github.com/repos/multiple_repo_org/testing-repo-private'
    #         },
    #         {
    #             "archived": False,
    #             "clone_url": 'https://github.com/multiple_repo_org/testing-repo-internal.git',
    #             "default_branch": "main",
    #             "description": None,
    #             "full_name": 'multiple_repo_org/testing-repo-internal',
    #             "hooks_url": 'https://github.com/repos/multiple_repo_org/testing-repo-internal/hooks',
    #             "language": None,
    #             "name": "testing-repo-internal",
    #             "owner": 'multiple_repo_org',
    #             "private": True,
    #             "url": 'https://github.com/repos/multiple_repo_org/testing-repo-internal'
    #         }
    #     ]
    #     assert result == test

    # def test_module_api_url_entered_as_empty(self):
    #     set_module_args({'access_token': 'token',
    #                      'organization': 'one_repo_org',
    #                      'api_url': ''})
    #     result = run_module()
    #     test = [
    #         {
    #             "archived": False,
    #             "clone_url": 'https://github.com/one_repo_org/testing-repo-private.git',
    #             "default_branch": "main",
    #             "description": None,
    #             "full_name": 'one_repo_org/testing-repo-private',
    #             "hooks_url": 'https://github.com/repos/one_repo_org/testing-repo-private/hooks',
    #             "language": None,
    #             "name": "testing-repo-private",
    #             "owner": 'one_repo_org',
    #             "private": True,
    #             "url": 'https://github.com/repos/one_repo_org/testing-repo-private'
    #         }
    #     ]
    #     assert result == test

    # def test_fail_api_call(self):
    #     set_module_args({'access_token': 'token',
    #                      'organization': 'one_repo_org',
    #                      'api_url': 'bad_url'})
    #     result = run_module()
    #     assert result == 'bad_url'

    # def test_fail_access_token(self):
    #     set_module_args({'access_token': 'bad_token',
    #                      'organization': 'one_repo_org',
    #                      'api_url': 'good_url'})
    #     result = run_module()
    #     assert result == 'bad_token'

    # def test_module_return_multiple_repo_api_url(self):
    #     set_module_args({'access_token': 'token',
    #                      'organization': 'multiple_repo_org',
    #                      'api_url': 'good_url'})
    #     result = run_module()
    #     test = [
    #         {
    #             "archived": False,
    #             "clone_url": 'good_url/multiple_repo_org/testing-repo-private.git',
    #             "default_branch": "main",
    #             "description": None,
    #             "full_name": 'multiple_repo_org/testing-repo-private',
    #             "hooks_url": 'good_url/repos/multiple_repo_org/testing-repo-private/hooks',
    #             "language": None,
    #             "name": "testing-repo-private",
    #             "owner": 'multiple_repo_org',
    #             "private": True,
    #             "url": 'good_url/repos/multiple_repo_org/testing-repo-private'
    #         },
    #         {
    #             "archived": False,
    #             "clone_url": 'good_url/multiple_repo_org/testing-repo-internal.git',
    #             "default_branch": "main",
    #             "description": None,
    #             "full_name": 'multiple_repo_org/testing-repo-internal',
    #             "hooks_url": 'good_url/repos/multiple_repo_org/testing-repo-internal/hooks',
    #             "language": None,
    #             "name": "testing-repo-internal",
    #             "owner": 'multiple_repo_org',
    #             "private": True,
    #             "url": 'good_url/repos/multiple_repo_org/testing-repo-internal'
    #         }
    #     ]
    #     assert result == test

    # def test_module_return_one_repo_api_url(self):
    #     set_module_args({'access_token': 'token',
    #                      'organization': 'one_repo_org',
    #                      'api_url': 'good_url'})
    #     result = run_module()
    #     test = [
    #         {
    #             "archived": False,
    #             "clone_url": 'good_url/one_repo_org/testing-repo-private.git',
    #             "default_branch": "main",
    #             "description": None,
    #             "full_name": 'one_repo_org/testing-repo-private',
    #             "hooks_url": 'good_url/repos/one_repo_org/testing-repo-private/hooks',
    #             "language": None,
    #             "name": "testing-repo-private",
    #             "owner": 'one_repo_org',
    #             "private": True,
    #             "url": 'good_url/repos/one_repo_org/testing-repo-private'
    #         }
    #     ]
    #     assert result == test

    # def test_module_return_empty_repo_api_url(self):
    #     set_module_args({'access_token': 'token',
    #                      'organization': 'no_repo_org',
    #                      'api_url': 'good_url'})
    #     result = run_module()
    #     test = []
    #     assert result == test
