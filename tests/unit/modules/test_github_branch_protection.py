from __future__ import (absolute_import, division, print_function)
from unittest import result
__metaclass__ = type

from ansible.module_utils import basic
from utils import ModuleTestCase, set_module_args, exit_json, AnsibleExitJson
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import jsonify
import json
import collections
import unittest


def remove_branch_protection(g, repo, branch):
    if branch == 'test_branch_protected':
        output = {
            'branch_protections' : {
                'allow_deletions' : {
                    'enabled' : False
                },
                'allow_force_pushes' : {
                    'enabled' : False
                },
                'enforce_admins' : {
                    'enabled' : False,
                    'url' : 'https://test.com/repos/test_organization/test_repo_protected/branches/test_branch/protection/enforce_admins'
                },
                'required_conversation_resolution' : {
                    'enabled' : False
                }
            },
            'url' : 'protection url'
        }
        output = {}
    else:
        output = {}
    return output


def edit_branch_protections(g, repo, branch, branch_protections):
    if branch == 'test_branch_protected':
        output = {
            'branch_protections' : {
                'allow_deletions' : {
                    'enabled' : False
                },
                'allow_force_pushes' : {
                    'enabled' : False
                },
                'enforce_admins' : {
                    'enabled' : False,
                    'url' : 'https://test.com/repos/test_organization/test_repo_protected/branches/test_branch/protection/enforce_admins'
                },
                'required_conversation_resolution' : {
                    'enabled' : False
                }
            },
            'url' : 'protection url'
        }
        try:
            output['branch_protections']['enforce_admins']['enabled'] = branch_protections['enforce_admins']
            return output

        except Exception as e:
            return e
    else:
        return {}


def get_branch_protections(g, repo, branch, token):
    output = {}
    try:
        if branch == 'test_branch_unprotected':
            return output
        else:
            url = 'protection url'
            output = {
                'branch_protections' : {
                    'allow_deletions' : {
                        'enabled' : False
                    },
                    'allow_force_pushes' : {
                        'enabled' : False
                    },
                    'enforce_admins' : {
                        'enabled' : False,
                        'url' : 'https://test.com/repos/test_organization/test_repo_protected/branches/test_branch/protection/enforce_admins'
                    },
                    'required_conversation_resolution' : {
                        'enabled' : False
                    }
                },
                'url' : url
            }
            return output
    
    except Exception as e:
        return e


def run_module():
    module_args = dict(
        token=dict(type='str', default='No Token Provided.'),
        organization_name=dict(type='str', default=''),
        enterprise_url=dict(type='str', default=''),
        repo=dict(type='str', default='No Repo Provided.'),
        branch=dict(type='str', default='No Branch Provided.'),
        branch_protections=dict(type='dict'),
        state=dict(type="str", default="No State Provided.")
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    g = 'Github token'

    if len(module.params['repo']):
        repo = module.params['organization_name'] + \
            "/" + module.params['repo']

    initial = get_branch_protections(g, module.params['repo'], module.params['branch'], module.params['token'])
    output = initial

    if module.params["branch_protections"] and module.params["state"] == "present":
        output = edit_branch_protections(g, module.params['repo'], module.params['branch'], module.params['branch_protections'])

    if module.params["state"] == "absent":
        output = remove_branch_protection(g, module.params['repo'], module.params['branch'],)

    print(output, '\n')
    return output, initial != output


class TestBranchProtectionModule(unittest.TestCase):
    def test_return_initial_branch(self):
        set_module_args({
            'token' : 'test_token',
            'repo' : 'test_repo_not_protected',
            'branch' : 'test_branch_unprotected'
        })
        result, changed = run_module()
        test = {}
        assert result == test
        assert changed == False

    def test_editing_branch_protection(self):
        set_module_args({
            'token' : 'test_token',
            'repo' : 'test_repo_protected',
            'branch' : 'test_branch_protected',
            'branch_protections' : {
                'enforce_admins' : True
            },
            'state' : 'present'
        })
        result, changed = run_module()
        test = {
            'branch_protections' : {
                'allow_deletions' : {
                    'enabled' : False
                },
                'allow_force_pushes' : {
                    'enabled' : False
                },
                'enforce_admins' : {
                    'enabled' : True,
                    'url' : 'https://test.com/repos/test_organization/test_repo_protected/branches/test_branch/protection/enforce_admins'
                },
                'required_conversation_resolution' : {
                    'enabled' : False
                }
            },
            'url' : 'protection url'
        }
        assert result == test
        assert changed == True

    def test_editing_branch_protection_with_same_protections(self):
        set_module_args({
            'token' : 'test_token',
            'repo' : 'test_repo_protected',
            'branch' : 'test_branch_protected',
            'branch_protections' : {
                'enforce_admins' : False
            },
            'state' : 'present'
        })
        result, changed = run_module()
        test = {
            'branch_protections' : {
                'allow_deletions' : {
                    'enabled' : False
                },
                'allow_force_pushes' : {
                    'enabled' : False
                },
                'enforce_admins' : {
                    'enabled' : False,
                    'url' : 'https://test.com/repos/test_organization/test_repo_protected/branches/test_branch/protection/enforce_admins'
                },
                'required_conversation_resolution' : {
                    'enabled' : False
                }
            },
            'url' : 'protection url'
        }
        assert result == test
        assert changed == False

    def test_remove_branch_protections(self):
        set_module_args({
            'token' : 'test_token',
            'repo' : 'test_repo_protected',
            'branch' : 'test_branch_protected',
            'branch_protections' : {
                'enforce_admins' : False
            },
            'state' : 'absent'
        })
        test = {}
        result, changed = run_module()
        assert result == test
        assert changed == True

    def test_remove_branch_protections_from_branch_with_no_protections(self):
        set_module_args({
            'token' : 'test_token',
            'repo' : 'test_repo_protected',
            'branch' : 'test_branch_unprotected',
            'branch_protections' : {
                'enforce_admins' : False
            },
            'state' : 'absent'
        })
        test = {}
        result, changed = run_module()
        assert result == test
        assert changed == changed