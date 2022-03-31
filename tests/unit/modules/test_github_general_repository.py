#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import collections
from email.policy import default
import json
from ansible.module_utils import basic
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_bytes
import unittest
# from numpy import outer
__metaclass__ = type


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
        repository=dict(type='str', default=''),
        team_name=dict(type='str', default=0),
        visibility=dict(type='str', default='public'),
        has_issues=dict(type='bool', default=True),
        has_wiki=dict(type='bool', default=True),
        auto_init=dict(type='bool', default=False),
        has_downloads=dict(type='bool', default=False),
        has_projects=dict(type='bool', default=True),
        allow_squash_merge=dict(type='bool', default=True),
        allow_merge_commit=dict(type='bool', default=True),
        allow_rebase_merge=dict(type='bool', default=True),
        delete_branch_on_merge=dict(type='bool', default=False),
        description=dict(type='str', default=''),
        homepage=dict(type='str', default=''),
        license_template=dict(type='str', default=''),
        gitignore_template=dict(type='str', default=''),
        state=dict(type='str', default='present'),
        check_mode=dict(type='bool', default=False)
    )

    valid_states = ["absent", "present"]
    valid_visibilities = ['public', 'private', 'internal']

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    initial = {}
    output_repo = {}

    if module.params['state'] not in valid_states:
        error_message = 'Invalid state: ' + module.params['state']
        return error_message, False
        module.exit_json(changed=False, err=error_message, failed=True)

    if module.params['visibility'] not in valid_visibilities:
        error_message = 'Invalid visibility: ' + module.params['visibility']
        return error_message, False
        module.exit_json(changed=False, err=error_message, failed=True)

    if module.params['api_url'] == '':
        g = module.params['access_token']
    else:
        g = module.params['access_token'] + module.params['api_url']

    getUrl = module.params['api_url'] + '/repos/' + \
        module.params['organization'] + \
        '/' + module.params['repository']

    org = {
        'teams': [
            {
                'name': 'team_1',
                'id': 1
            },
            {
                'name': 'team_2',
                'id': 2
            }
        ]
    }

    body = {}
    payload = {}

    req = {
        'status_code': 404 
    }
    if module.params['access_token'] == 'good_token':
        req['status_code'] = 200
        body = {
            "name": 'Hello-Ansible',
            "full_name": 'Ansible/Hello-Ansible',
            "owner": {
                'login': 'Ansible',
                'id': -1,
                'type': 'User',
                'site_admin': False
            },
            "description": 'Test Description',
            "visibility": 'private',
            "archived": True,
            "language": None,
            "url": "https://api.github.com/repos/Ansible/Hello-Ansible",
            "default_branch": True,
            "hooks_url": "https://api.github.com/repos/Ansible/Hello-Ansible/hooks",
            "clone_url": "https://github.com/Ansible/Hello-Ansible.git",
            "allow_merge_commit": True,
            "allow_rebase_merge": True,
            "allow_squash_merge": True,
            "delete_branch_on_merge": False,
            "has_issues": True,
            "has_downloads": False,
            "has_wiki": True,
            "has_projects": True,
            "homepage": ""
        }

    # req = requests.get(
    #     getUrl, headers={'Content-type': 'application/json', 'Authorization': 'Bearer ' + module.params['access_token']})

    if req['status_code'] == 404:  # repository does NOT exist
        if module.params['state'] == 'present':
            # org = g.get_organization(module.params['organization'])
            for team in org['teams']:
                if team['name'] == module.params['team_name']:
                    if module.check_mode:
                        if module.params['api_url']:
                            noApiurl = str(module.params['api_url']).replace(
                                "/api/v3", "")
                            clone_url = "%s/%s/%s.git" % (
                                noApiurl, module.params['organization'], module.params['repository'])
                            url = "%s/repos/%s/%s" % (
                                module.params['api_url'], module.params['organization'], module.params['repository'])
                            hooks_url = "%s/hooks" % (url)
                        else:
                            clone_url = "https://github.com/%s/%s.git" % (
                                module.params['organization'], module.params['repository'])
                            url = "https://github.com/api/v3/repos/%s/%s" % (
                                module.params['organization'], module.params['repository'])
                            hooks_url = "%s/hooks" % (url)
                        full_name = "%s/%s" % (
                            module.params['organization'], module.params['repository'])

                        is_private = module.params['visibility']

                        output_repo = {
                            "allow_merge_commit": module.params['allow_merge_commit'],
                            "allow_rebase_merge": module.params['allow_rebase_merge'],
                            "allow_squash_merge": module.params['allow_squash_merge'],
                            "archived": False,
                            "clone_url": clone_url,
                            "default_branch": "main",
                            "delete_branch_on_merge": module.params['delete_branch_on_merge'],
                            "description": module.params['description'],
                            "full_name": full_name,
                            "has_downloads": module.params['has_downloads'],
                            "has_issues": module.params['has_issues'],
                            "has_projects": module.params['has_projects'],
                            "has_wiki": module.params['has_wiki'],
                            "homepage": module.params['homepage'],
                            "hooks_url": hooks_url,
                            "language": None,
                            "name": module.params['repository'],
                            "owner": module.params['organization'],
                            "visibility": is_private,
                            "url": url
                        }
                    else:
                        url = module.params['api_url'] + '/orgs/' + \
                            module.params['organization'] + '/repos'

                        payload = {
                            "name": module.params['repository'],
                            "description": module.params['description'],
                            "homepage": module.params['homepage'],
                            "private": module.params['visibility'],
                            "has_issues": module.params['has_issues'],
                            "has_wiki": module.params['has_wiki'],
                            "has_downloads": module.params['has_downloads'],
                            "has_projects": module.params['has_projects'],
                            "team_id": team['id'],
                            "visibility": module.params['visibility'],
                            "auto_init": module.params['auto_init'],
                            "license_template": module.params['license_template'],
                            "gitignore_template": module.params['gitignore_template'],
                            "allow_squash_merge": module.params['allow_squash_merge'],
                            "allow_merge_commit": module.params['allow_merge_commit'],
                            "allow_rebase_merge": module.params['allow_rebase_merge'],
                            "delete_branch_on_merge": module.params['delete_branch_on_merge']
                        }
                        # output = payload.copy()

                        # requests.post(
                        #     url, json=payload, headers={'Content-type': 'application/json', 'Authorization': 'Bearer ' + module.params['access_token']})
    elif req['status_code'] == 200:  # Repository DOES exist
        # body = json.loads(req.text)
        initial = {
            "name": body['name'],
            "full_name": body['full_name'],
            "owner": body['owner']['login'],
            "description": body['description'],
            "visibility": body['visibility'],
            "archived": body['archived'],
            "language": body['language'],
            "url": body['url'],
            "default_branch": body['default_branch'],
            "hooks_url": body['hooks_url'],
            "clone_url": body['clone_url'],
            "allow_merge_commit": body['allow_merge_commit'],
            "allow_rebase_merge": body['allow_rebase_merge'],
            "allow_squash_merge": body['allow_squash_merge'],
            "delete_branch_on_merge": body['delete_branch_on_merge'],
            "has_issues": body['has_issues'],
            "has_downloads": body['has_downloads'],
            "has_wiki": body['has_wiki'],
            "has_projects": body['has_projects'],
            "homepage": body['homepage']
        }

        if module.params['state'] == 'present':
            if module.params['check_mode']:
                output_repo = initial.copy()
                output_repo['visibility'] = module.params["visibility"]
                output_repo['description'] = module.params["description"]
                output_repo['homepage'] = module.params["homepage"]
                output_repo['has_issues'] = module.params["has_issues"]
                output_repo['has_wiki'] = module.params["has_wiki"]
                output_repo['has_downloads'] = module.params["has_downloads"]
                output_repo['has_projects'] = module.params["has_projects"]
                output_repo['allow_merge_commit'] = module.params["allow_merge_commit"]
                output_repo['allow_rebase_merge'] = module.params["allow_rebase_merge"]
                output_repo['allow_squash_merge'] = module.params["allow_squash_merge"]
                output_repo['delete_branch_on_merge'] = module.params["delete_branch_on_merge"]
            else:
                # org = g.get_organization(module.params['organization'])
                for team in org['teams']:
                    if team['name'] == module.params['team_name']:
                        url = module.params['api_url'] + '/repos/' + \
                            module.params['organization'] + \
                            '/' + module.params['repository']
                        payload = {
                            "name": module.params['repository'],
                            "description": module.params['description'],
                            "homepage": module.params['homepage'],
                            "has_issues": module.params['has_issues'],
                            "has_wiki": module.params['has_wiki'],
                            "has_downloads": module.params['has_downloads'],
                            "has_projects": module.params['has_projects'],
                            "team_id": team['id'],
                            "visibility": module.params['visibility'],
                            "auto_init": module.params['auto_init'],
                            "license_template": module.params['license_template'],
                            "gitignore_template": module.params['gitignore_template'],
                            "allow_squash_merge": module.params['allow_squash_merge'],
                            "allow_merge_commit": module.params['allow_merge_commit'],
                            "allow_rebase_merge": module.params['allow_rebase_merge'],
                            "delete_branch_on_merge": module.params['delete_branch_on_merge']
                        }
                        output = payload.copy()
                        # requests.patch(url, json=payload, headers={
                        #     'Content-type': 'application/json', 'Authorization': 'Bearer ' + module.params['access_token'], 'Accept': 'application/vnd.github.v3+json'})
        elif module.params['state'] == 'absent':
            if not module.params['check_mode']:
                output = {}
                # g.get_organization(module.params['organization']).get_repo(
                #     module.params['repository']).delete()
            else:
                output_repo = {}

    finalReq = {
        'status_code': 200
    }
    if module.params['access_token'] == 'not_working_token' or module.params['state'] == 'absent':
        finalReq['status_code'] = 404
    # finalReq = requests.get(
    #     getUrl, headers={'Content-type': 'application/json', 'Authorization': 'Bearer ' + module.params['access_token']})

    if finalReq['status_code'] == 404:
        output = {}
    else:
        # body = json.loads(finalReq.text)
        if not module.params['check_mode']:
            output = {
                "name": payload['name'],
                "full_name": body['full_name'],
                "owner": body['owner']['login'],
                "description": payload['description'],
                "visibility": body['visibility'],
                "archived": body['archived'],
                "language": body['language'],
                "url": body['url'],
                "default_branch": body['default_branch'],
                "hooks_url": body['hooks_url'],
                "clone_url": body['clone_url'],
                "allow_merge_commit": payload['allow_merge_commit'],
                "allow_rebase_merge": payload['allow_rebase_merge'],
                "allow_squash_merge": payload['allow_squash_merge'],
                "delete_branch_on_merge": payload['delete_branch_on_merge'],
                "has_issues": payload['has_issues'],
                "has_downloads": payload['has_downloads'],
                "has_wiki": payload['has_wiki'],
                "has_projects": payload['has_projects'],
                "homepage": payload['homepage']
            }
    if module.params['check_mode']:
        return output_repo, initial!=output_repo
        # module.exit_json(repo=output_repo, changed=initial != output_repo)
    else:
        return output, initial!=output
        # module.exit_json(repo=output, changed=initial != output)


class TestGeneralRepositoryModule(unittest.TestCase):
    def test_return_initial_repo(self):
        set_module_args({
            'access_token' : 'good_token',
            'repository' : 'Hello-Ansible',
            'organization' : 'Ansible',
            'team_name': 'team_1',
            'description': 'Test Description',
            'visibility': 'private',
            'state' : 'present'
        })
        result, changed = run_module()
        test = {
            "name": 'Hello-Ansible',
            "full_name": 'Ansible/Hello-Ansible',
            "owner": 'Ansible',
            "description": 'Test Description',
            "visibility": 'private',
            "archived": True,
            "language": None,
            "url": "https://api.github.com/repos/Ansible/Hello-Ansible",
            "default_branch": True,
            "hooks_url": "https://api.github.com/repos/Ansible/Hello-Ansible/hooks",
            "clone_url": "https://github.com/Ansible/Hello-Ansible.git",
            "allow_merge_commit": True,
            "allow_rebase_merge": True,
            "allow_squash_merge": True,
            "delete_branch_on_merge": False,
            "has_issues": True,
            "has_downloads": False,
            "has_wiki": True,
            "has_projects": True,
            "homepage": ""
        }

        assert result == test
        assert changed == False

    def test_changing_one_variable(self):
        set_module_args({
            'access_token' : 'good_token',
            'repository' : 'Hello-Ansible',
            'organization' : 'Ansible',
            'description': 'New Description',
            'team_name': 'team_1',
            'visibility': 'private',
            'state' : 'present'
        })
        result, changed = run_module()
        test = {
            "name": 'Hello-Ansible',
            "full_name": 'Ansible/Hello-Ansible',
            "owner": 'Ansible',
            "description": 'New Description',
            "visibility": 'private',
            "archived": True,
            "language": None,
            "url": "https://api.github.com/repos/Ansible/Hello-Ansible",
            "default_branch": True,
            "hooks_url": "https://api.github.com/repos/Ansible/Hello-Ansible/hooks",
            "clone_url": "https://github.com/Ansible/Hello-Ansible.git",
            "allow_merge_commit": True,
            "allow_rebase_merge": True,
            "allow_squash_merge": True,
            "delete_branch_on_merge": False,
            "has_issues": True,
            "has_downloads": False,
            "has_wiki": True,
            "has_projects": True,
            "homepage": ""
        }
        print(result, '\n')
        print(test)

        assert result == test
        assert changed == True

    def test_changing_multiple_variables(self):
        set_module_args({
            'access_token' : 'good_token',
            'repository' : 'Hello-Ansible',
            'organization' : 'Ansible',
            'description': 'New Description',
            'allow_merge_commit': False,
            'team_name': 'team_1',
            'visibility': 'private',
            'state' : 'present'
        })
        result, changed = run_module()
        test = {
            "name": 'Hello-Ansible',
            "full_name": 'Ansible/Hello-Ansible',
            "owner": 'Ansible',
            "description": 'New Description',
            "visibility": 'private',
            "archived": True,
            "language": None,
            "url": "https://api.github.com/repos/Ansible/Hello-Ansible",
            "default_branch": True,
            "hooks_url": "https://api.github.com/repos/Ansible/Hello-Ansible/hooks",
            "clone_url": "https://github.com/Ansible/Hello-Ansible.git",
            "allow_merge_commit": False,
            "allow_rebase_merge": True,
            "allow_squash_merge": True,
            "delete_branch_on_merge": False,
            "has_issues": True,
            "has_downloads": False,
            "has_wiki": True,
            "has_projects": True,
            "homepage": ""
        }

        assert result == test
        assert changed == True

    def test_deleting_repository(self):
        set_module_args({
            'access_token' : 'good_token',
            'repository' : 'Hello-Ansible',
            'organization' : 'Ansible',
            'description': 'New Description',
            'allow_merge_commit': False,
            'team_name': 'team_1',
            'state' : 'absent'
        })
        result, changed = run_module()
        test = {}

        assert result == test
        assert changed == True

    def test_deleting_repository_that_does_not_exit(self):
        set_module_args({
            'access_token' : 'good_token',
            'repository' : 'Goodbye-Ansible',
            'organization' : 'Ansible',
            'description': 'New Description',
            'allow_merge_commit': False,
            'team_name': 'team_1',
            'state' : 'absent'
        })
        result, changed = run_module()
        test = {}

        assert result == test
        assert changed == True

    def test_error_message_state_choices(self):
        set_module_args({
            'access_token' : 'good_token',
            'repository' : 'Goodbye-Ansible',
            'organization' : 'Ansible',
            'description': 'New Description',
            'allow_merge_commit': False,
            'team_name': 'team_1',
            'state' : 'Maybe'
        })
        result, changed = run_module()
        test = 'Invalid state: Maybe'

        assert result == test
        assert changed == False

    def test_error_message_visibility_choices(self):
        set_module_args({
            'access_token' : 'good_token',
            'repository' : 'Goodbye-Ansible',
            'organization' : 'Ansible',
            'description': 'New Description',
            'allow_merge_commit': False,
            'team_name': 'team_1',
            'visibility': 'Publicly Open',
            'state' : 'present'
        })
        result, changed = run_module()
        test = 'Invalid visibility: Publicly Open'

        assert result == test
        assert changed == False

    def test_changing_one_variable_check_mode(self):
        set_module_args({
            'access_token' : 'good_token',
            'repository' : 'Hello-Ansible',
            'organization' : 'Ansible',
            'description': 'New Description',
            'team_name': 'team_1',
            'state' : 'present',
            'check_mode': True
        })
        result, changed = run_module()
        test = {
            "name": 'Hello-Ansible',
            "full_name": 'Ansible/Hello-Ansible',
            "owner": 'Ansible',
            "description": 'New Description',
            "visibility": 'public',
            "archived": True,
            "language": None,
            "url": "https://api.github.com/repos/Ansible/Hello-Ansible",
            "default_branch": True,
            "hooks_url": "https://api.github.com/repos/Ansible/Hello-Ansible/hooks",
            "clone_url": "https://github.com/Ansible/Hello-Ansible.git",
            "allow_merge_commit": True,
            "allow_rebase_merge": True,
            "allow_squash_merge": True,
            "delete_branch_on_merge": False,
            "has_issues": True,
            "has_downloads": False,
            "has_wiki": True,
            "has_projects": True,
            "homepage": ""
        }
        print(result, '\n')
        print(test)

        assert result == test
        assert changed == True

    def test_changing_multiple_variables_check_mode(self):
        set_module_args({
            'access_token' : 'good_token',
            'repository' : 'Hello-Ansible',
            'organization' : 'Ansible',
            'description': 'New Description',
            'allow_merge_commit': False,
            'team_name': 'team_1',
            'state' : 'present',
            'check_mode': True
        })
        result, changed = run_module()
        test = {
            "name": 'Hello-Ansible',
            "full_name": 'Ansible/Hello-Ansible',
            "owner": 'Ansible',
            "description": 'New Description',
            "visibility": 'public',
            "archived": True,
            "language": None,
            "url": "https://api.github.com/repos/Ansible/Hello-Ansible",
            "default_branch": True,
            "hooks_url": "https://api.github.com/repos/Ansible/Hello-Ansible/hooks",
            "clone_url": "https://github.com/Ansible/Hello-Ansible.git",
            "allow_merge_commit": False,
            "allow_rebase_merge": True,
            "allow_squash_merge": True,
            "delete_branch_on_merge": False,
            "has_issues": True,
            "has_downloads": False,
            "has_wiki": True,
            "has_projects": True,
            "homepage": ""
        }

        assert result == test
        assert changed == True

    def test_deleting_repository_check_mode(self):
        set_module_args({
            'access_token' : 'good_token',
            'repository' : 'Hello-Ansible',
            'organization' : 'Ansible',
            'description': 'New Description',
            'allow_merge_commit': False,
            'team_name': 'team_1',
            'state' : 'absent',
            'check_mode': True
        })
        result, changed = run_module()
        test = {}

        assert result == test
        assert changed == True

    def test_deleting_repository_that_does_not_exit_check_mode(self):
        set_module_args({
            'access_token' : 'good_token',
            'repository' : 'Goodbye-Ansible',
            'organization' : 'Ansible',
            'description': 'New Description',
            'allow_merge_commit': False,
            'team_name': 'team_1',
            'state' : 'absent',
            'check_mode': True
        })
        result, changed = run_module()
        test = {}

        assert result == test
        assert changed == True