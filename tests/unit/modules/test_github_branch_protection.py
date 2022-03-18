from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils import basic
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import jsonify
from ansible.module_utils._text import to_bytes
import json
import collections
import unittest


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


def absent_branch_protection(g, repo, branch):
    output = dict()
    return output


def absent_branch_protection_check_mode():
    output = dict()
    return output


def present_branch_protection_check_mode(initial, branch_protections, api_url, repository, organization, branch):
    if initial != {}:
        output = initial.copy()
    else:
        output = {
            "allow_deletions": {
                "enabled": False
            },
            "allow_force_pushes": {
                "enabled": False
            },
            "enforce_admins": {
                "enabled": False,
                "url": "https://" + (api_url if api_url else "github.com") + "/repos/" +
                       organization + "/" + repository + "/branches/" + branch + "/protection/enforce_admins"
            },
            "required_conversation_resolution": {
                "enabled": False
            },
            "required_linear_history": {
                "enabled": False
            },
            "required_pull_request_reviews": {
                "dismiss_stale_reviews": False,
                "dismissal_restrictions": {
                    "teams": [],
                    "teams_url": "https://" + (api_url if api_url else "github.com") + "/repos/" +
                                 organization + "/" + repository + "/branches/" + branch + "/protection/dismissal_restrictions/teams",
                    "url": "https://" + (api_url if api_url else "github.com") + "/repos/" +
                           organization + "/" + repository + "/branches/" + branch + "/protection/dismissal_restrictions",
                    "users": [],
                    "users_url": "https://" + (api_url if api_url else "github.com") + "/repos/" +
                                 organization + "/" + repository + "/branches/" + branch + "/protection/dismissal_restrictions/users"
                },
                "require_code_owner_reviews": False,
                "required_approving_review_count": 0,
                "url": "https://" + (api_url if api_url else "github.com") + "/repos/" +
                       organization + "/" + repository + "/branches/" + branch + "/protection/required_pull_request_reviews"
            },
            "required_signatures": {
                "enabled": False,
                "url": "https://" + (api_url if api_url else "github.com") + "/repos/" +
                       organization + "/" + repository + "/branches/" + branch + "/protection/required_signatures"
            },
            "required_status_checks": {
                "contexts": [],
                "contexts_url": "https://" + (api_url if api_url else "github.com") + "/repos/" +
                                organization + "/" + repository + "/branches/" + branch + "/protection/required_status_checks/contexts",
                "strict": False,
                "url": "https://" + (api_url if api_url else "github.com") + "/repos/" +
                       organization + "SEP/" + repository + "/branches/" + branch + "/protection/required_status_checks"
            },
            "restrictions": {
                "apps": [],
                "apps_url": "https://" + (api_url if api_url else "github.com") + "/repos/" +
                            organization + "/" + repository + "/branches/" + branch + "/protection/restrictions/apps",
                "teams": [],
                "teams_url": "https://" + (api_url if api_url else "github.com") + "/repos/" +
                             organization + "/" + repository + "/branches/" + branch + "/protection/restrictions/teams",
                "url": "https://" + (api_url if api_url else "github.com") + "/repos/" +
                       organization + "/" + repository + "/branches/" + branch + "/protection/restrictions",
                "users": [],
                "users_url": "https://" + (api_url if api_url else "github.com") + "/repos/" +
                             organization + "/" + repository + "/branches/" + branch + "/protection/restrictions/users"
            },
            "url": "https://" + (api_url if api_url else "github.com") + "/repos/" +
                   organization + "/" + repository + "/branches/" + branch + "/protection"
        }

    output['enforce_admins']['enabled'] = branch_protections['enforce_admins']
    output['required_pull_request_reviews']['dismiss_stale_reviews'] = branch_protections['dismiss_stale_reviews']
    output['required_status_checks']['strict'] = branch_protections['strict']
    output['required_status_checks']['contexts'] = branch_protections['contexts']
    output['required_pull_request_reviews']['dismiss_stale_reviews'] = branch_protections['dismiss_stale_reviews']
    output['required_pull_request_reviews']['require_code_owner_reviews'] = branch_protections['require_code_owner_reviews']
    output['required_pull_request_reviews']['required_approving_review_count'] = branch_protections['required_approving_review_count']

    for team in branch_protections["dismissal_teams"]:
        if next((x for x in output['required_pull_request_reviews']['dismissal_restrictions']['teams'] if x["name"] == team), None) is None:
            new_team = {
                "description": "This is a team to test branch protection functionality",
                "html_url": "https://" + (api_url if api_url else "github.com") + "/repos/" +
                            organization + "/" + repository + "/branches/" + branch + "/protection/dismissal_restrictions/teams",
                "id": 0,
                "members_url": "https://" + (api_url if api_url else "github.com") + "/organizations/0/team/0/members{/member}",
                "name": team,
                "node_id": "NodeID",
                "parent": None,
                "permission": "pull",
                "privacy": "closed",
                "repositories_url": "https://" + (api_url if api_url else "github.com") + "/organizations/0/team/0/repos",
                "slug": team,
                "url": "https://" + (api_url if api_url else "github.com") + "/organizations/0/team/0"
            }
            output['required_pull_request_reviews']['dismissal_restrictions']['teams'].append(new_team)

    for team in output['required_pull_request_reviews']['dismissal_restrictions']['teams']:
        if team['name'] not in branch_protections['dismissal_teams']:
            output['required_pull_request_reviews']['dismissal_restrictions']['teams'].remove(team)

    for user in branch_protections["dismissal_users"]:
        if next((x for x in output['required_pull_request_reviews']['dismissal_restrictions']['users'] if x["login"] == user), None) is None:
            new_user = {
                "avatar_url": "https://avatars." + (api_url if api_url else "github.com") + "/u/108?",
                "events_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/events{/privacy}",
                "followers_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/followers",
                "following_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/following{/other_user}",
                "gists_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/gists{/gist_id}",
                "gravatar_id": "",
                "html_url": "https://" + (api_url if api_url else "github.com") + "/" + user,
                "id": 000,
                "login": user,
                "node_id": "NodeID",
                "organizations_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/orgs",
                "received_events_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/received_events",
                "repos_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/repos",
                "site_admin": False,
                "starred_url": "https://" + (api_url if api_url else "github.com") + "//users/" + user + "/starred{/owner}{/repo}",
                "subscriptions_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/subscriptions",
                "type": "User",
                "url": "https://" + (api_url if api_url else "github.com") + "/users/" + user
            }
            output['required_pull_request_reviews']['dismissal_restrictions']['users'].append(new_user)

    for user in output['required_pull_request_reviews']['dismissal_restrictions']['users']:
        if user['login'] not in branch_protections['dismissal_users']:
            output['required_pull_request_reviews']['dismissal_restrictions']['users'].remove(user)

    for team in branch_protections["team_push_restrictions"]:
        if next((x for x in output['restrictions']['teams'] if x["name"] == team), None) is None:
            new_team = {
                "description": "This is a team to test branch protection functionality",
                "html_url": "https://" + (api_url if api_url else "github.com") + "/orgs/" + organization + "/teams/" + team,
                "id": 0,
                "members_url": "https://" + (api_url if api_url else "github.com") + "/organizations/0/team/0/members{/member}",
                "name": team,
                "node_id": "NodeID",
                "parent": None,
                "permission": "pull",
                "privacy": "closed",
                "repositories_url": "https://" + (api_url if api_url else "github.com") + "/organizations/0/team/0/repos",
                "slug": team,
                "url": "https://" + (api_url if api_url else "github.com") + "/organizations/0/team/0"
            }
            output['restrictions']['teams'].append(new_team)

    for team in output['restrictions']['teams']:
        if team['name'] not in branch_protections['team_push_restrictions']:
            output['restrictions']['teams'].remove(team)

    for user in branch_protections["user_push_restrictions"]:
        if next((x for x in output['restrictions']['users'] if x["login"] == user), None) is None:
            new_user = {
                "avatar_url": "https://" + (api_url if api_url else "github.com") + "/u/0",
                "events_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/events{/privacy}",
                "followers_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/followers",
                "following_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/following{/other_user}",
                "gists_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/gists{/gist_id}",
                "gravatar_id": "",
                "html_url": "https://" + (api_url if api_url else "github.com") + "/" + user,
                "id": 0,
                "login": user,
                "node_id": "NodeID",
                "organizations_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/orgs",
                "received_events_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/received_events",
                "repos_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/repos",
                "site_admin": False,
                "starred_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/starred{/owner}{/repo}",
                "subscriptions_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/subscriptions",
                "type": "User",
                "url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + ""
            }
            output['restrictions']['users'].append(new_user)

    for user in output['restrictions']['users']:
        if user['login'] not in branch_protections['user_push_restrictions']:
            output['restrictions']['users'].remove(user)

    output['required_pull_request_reviews']['dismissal_restrictions']['users'] = branch_protections['dismissal_users']
    output['required_pull_request_reviews']['dismissal_restrictions']['teams'] = branch_protections['dismissal_teams']
    output['restrictions']['users'] = branch_protections['user_push_restrictions']
    output['restrictions']['teams'] = branch_protections['team_push_restrictions']

    return output


def present_branch_protections(g, repo, branch, branch_protections):
    output = g.copy()
    try:
        output['enforce_admins']['enabled'] = branch_protections['enforce_admins']
        output['required_pull_request_reviews']['dismiss_stale_reviews'] = branch_protections['dismiss_stale_reviews']
        output['required_status_checks']['strict'] = branch_protections['strict']
        output['required_status_checks']['contexts'] = branch_protections['contexts']
        output['required_pull_request_reviews']['dismiss_stale_reviews'] = branch_protections['dismiss_stale_reviews']
        output['required_pull_request_reviews']['require_code_owner_reviews'] = branch_protections['require_code_owner_reviews']
        output['required_pull_request_reviews']['required_approving_review_count'] = branch_protections['required_approving_review_count']
        output['required_pull_request_reviews']['dismissal_restrictions']['users'] = branch_protections['dismissal_users']
        output['required_pull_request_reviews']['dismissal_restrictions']['teams'] = branch_protections['dismissal_teams']
        output['restrictions']['users'] = branch_protections['user_push_restrictions']
        output['restrictions']['teams'] = branch_protections['team_push_restrictions']
        return output
    except Exception as e:
        return e


def get_branch_protections(g, repo, branch, token):
    output = {}
    try:
        if repo == 'not_protected':
            return output
        else:
            output = {
                "allow_deletions": {
                    "enabled": False
                },
                "allow_force_pushes": {
                    "enabled": False
                },
                "enforce_admins": {
                    "enabled": False,
                    "url": "https://" + "api.github.com" + "/repos/" + repo + "/branches/" + branch + "/protection/enforce_admins"
                },
                "required_conversation_resolution": {
                    "enabled": False
                },
                "required_linear_history": {
                    "enabled": False
                },
                "required_pull_request_reviews": {
                    "dismiss_stale_reviews": False,
                    "dismissal_restrictions": {
                        "teams": [],
                        "teams_url": "https://" + "api.github.com" + "/repos/" + repo + "/branches/" + branch + "/protection/dismissal_restrictions/teams",
                        "url": "https://" + "api.github.com" + "/repos/" + repo + "/branches/" + branch + "/protection/dismissal_restrictions",
                        "users": [],
                        "users_url": "https://" + "api.github.com" + "/repos/" + repo + "/branches/" + branch + "/protection/dismissal_restrictions/users"
                    },
                    "require_code_owner_reviews": False,
                    "required_approving_review_count": 0,
                    "url": "https://" + "api.github.com" + "/repos/" + repo + "/branches/" + branch + "/protection/required_pull_request_reviews"
                },
                "required_signatures": {
                    "enabled": False,
                    "url": "https://" + "api.github.com" + "/repos/" + repo + "/branches/" + branch + "/protection/required_signatures"
                },
                "required_status_checks": {
                    "contexts": [],
                    "contexts_url": "https://" + "api.github.com" + "/repos/" + repo + "/branches/" + branch + "/protection/required_status_checks/contexts",
                    "strict": False,
                    "url": "https://" + "api.github.com" + "/repos/" + repo + "/branches/" + branch + "/protection/required_status_checks"
                },
                "restrictions": {
                    "apps": [],
                    "apps_url": "https://" + "api.github.com" + "/repos/" + repo + "/branches/" + branch + "/protection/restrictions/apps",
                    "teams": [],
                    "teams_url": "https://" + "api.github.com" + "/repos/" + repo + "/branches/" + branch + "/protection/restrictions/teams",
                    "url": "https://" + "api.github.com" + "/repos/" + repo + "/branches/" + branch + "/protection/restrictions",
                    "users": [],
                    "users_url": "https://" + "api.github.com" + "/repos/" + repo + "/branches/" + branch + "/protection/restrictions/users"
                },
                "url": "https://" + "api.github.com" + "/repos/" + repo + "/branches/" + branch + "/protection"
            }
            return output

    except Exception as e:
        return e


def run_module():
    module_args = dict(
        access_token=dict(type='str', required=True, no_log=True),
        organization=dict(
            type='str', required=True),
        api_url=dict(type='str', default=''),
        repository=dict(type='str', required=True),
        branch=dict(type='str', required=True),
        branch_protections=dict(type='dict'),
        state=dict(type="str", default="present"),
        check_mode=dict(type='bool', default=False)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if(module.params['api_url'] == ''):
        g = module.params['access_token']
    else:
        g = module.params['access_token'] + module.params['api_url']

    if len(module.params['repository']):
        module.params['repository'] = module.params['organization'] + \
            "/" + module.params['repository']

    initial = get_branch_protections(g, module.params['repository'], module.params['branch'], module.params['access_token'])
    output = dict()
    changed = False
    if not initial:
        initial = {}

    if module.params["state"] == "present":
        if module.params['check_mode']:
            output = present_branch_protection_check_mode(
                initial,
                module.params['branch_protections'],
                module.params['api_url'],
                module.params['repository'],
                module.params['organization'],
                module.params['branch']
            )
        else:
            output = present_branch_protections(initial, module.params['repository'], module.params['branch'], module.params['branch_protections'])

    if module.params["state"] == "absent":
        if module.params['check_mode']:
            output = absent_branch_protection_check_mode()
        else:
            output = absent_branch_protection(initial, module.params['repository'], module.params['branch'])

    result = dict(
        changed=initial != output,
        fact=''
    )

    initial = get_branch_protections(g, module.params['repository'], module.params['branch'], module.params['access_token'])

    if output != initial:
        changed = True

    return output, changed


class TestBranchProtectionModule(unittest.TestCase):
    def test_return_passing_arguments(self):
        set_module_args({
            'access_token': 'test_token',
            'organization': 'org_name',
            'repository': 'not_protected',
            'branch': 'test_branch_unprotected',
            'branch_protections': {
                'strict': True
            }
        })
        result, changed = run_module()
        self.assertRaises(AnsibleExitJson)

    def test_editing_branch_protection_with_same_protections(self):
        set_module_args({
            'access_token': 'test_token',
            'organization': 'org_name',
            'repository': 'test_repo_protected',
            'branch': 'test_branch_protected',
            'branch_protections': {
                'strict': False,
                'contexts': [],
                'enforce_admins': False,
                'dismissal_users': [],
                'dismissal_teams': [],
                'dismiss_stale_reviews': False,
                'require_code_owner_reviews': False,
                'required_approving_review_count': 0,
                'user_push_restrictions': [],
                'team_push_restrictions': [],
            },
            'state': 'present'
        })
        result, changed = run_module()
        test = {
            "allow_deletions": {
                "enabled": False
            },
            "allow_force_pushes": {
                "enabled": False
            },
            "enforce_admins": {
                "enabled": False,
                "url": "https://" + "api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/enforce_admins"
            },
            "required_conversation_resolution": {
                "enabled": False
            },
            "required_linear_history": {
                "enabled": False
            },
            "required_pull_request_reviews": {
                "dismiss_stale_reviews": False,
                "dismissal_restrictions": {
                    "teams": [],
                    "teams_url": "https://api.github.com/repos/org_name/test_repo_protected/branches/" +
                                 "test_branch_protected/protection/dismissal_restrictions/teams",
                    "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/dismissal_restrictions",
                    "users": [],
                    "users_url": "https://api.github.com/repos/org_name/test_repo_protected/branches/" +
                                 "test_branch_protected/protection/dismissal_restrictions/users"
                },
                "require_code_owner_reviews": False,
                "required_approving_review_count": 0,
                "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/required_pull_request_reviews"
            },
            "required_signatures": {
                "enabled": False,
                "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/required_signatures"
            },
            "required_status_checks": {
                "contexts": [],
                "contexts_url": "https://api.github.com/repos/org_name/test_repo_protected/branches/" +
                                "test_branch_protected/protection/required_status_checks/contexts",
                "strict": False,
                "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/required_status_checks"
            },
            "restrictions": {
                "apps": [],
                "apps_url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/restrictions/apps",
                "teams": [],
                "teams_url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/restrictions/teams",
                "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/restrictions",
                "users": [],
                "users_url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/restrictions/users"
            },
            "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection"
        }
        assert result == test
        assert changed is False

    def test_editing_branch_protection(self):
        set_module_args({
            'access_token': 'test_token',
            'organization': 'org_name',
            'repository': 'test_repo_protected',
            'branch': 'test_branch_protected',
            'branch_protections': {
                'strict': False,
                'contexts': [],
                'enforce_admins': True,
                'dismissal_users': [],
                'dismissal_teams': [],
                'dismiss_stale_reviews': False,
                'require_code_owner_reviews': False,
                'required_approving_review_count': 0,
                'user_push_restrictions': [],
                'team_push_restrictions': [],
            },
            'state': 'present'
        })
        result, changed = run_module()
        test = {
            "allow_deletions": {
                "enabled": False
            },
            "allow_force_pushes": {
                "enabled": False
            },
            "enforce_admins": {
                "enabled": True,
                "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/enforce_admins"
            },
            "required_conversation_resolution": {
                "enabled": False
            },
            "required_linear_history": {
                "enabled": False
            },
            "required_pull_request_reviews": {
                "dismiss_stale_reviews": False,
                "dismissal_restrictions": {
                    "teams": [],
                    "teams_url": "https://api.github.com/repos/org_name/test_repo_protected/" +
                                 "branches/test_branch_protected/protection/dismissal_restrictions/teams",
                    "url": "https://api.github.com/repos/org_name/test_repo_protected/" +
                           "branches/test_branch_protected/protection/dismissal_restrictions",
                    "users": [],
                    "users_url": "https://api.github.com/repos/org_name/test_repo_protected/" +
                                 "branches/test_branch_protected/protection/dismissal_restrictions/users"
                },
                "require_code_owner_reviews": False,
                "required_approving_review_count": 0,
                "url": "https://api.github.com/repos/org_name/test_repo_protected/" +
                       "branches/test_branch_protected/protection/required_pull_request_reviews"
            },
            "required_signatures": {
                "enabled": False,
                "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/required_signatures"
            },
            "required_status_checks": {
                "contexts": [],
                "contexts_url": "https://api.github.com/repos/org_name/test_repo_protected/" +
                                "branches/test_branch_protected/protection/required_status_checks/contexts",
                "strict": False,
                "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/required_status_checks"
            },
            "restrictions": {
                "apps": [],
                "apps_url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/restrictions/apps",
                "teams": [],
                "teams_url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/restrictions/teams",
                "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/restrictions",
                "users": [],
                "users_url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/restrictions/users"
            },
            "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection"
        }
        assert result == test
        assert changed is True

    def test_remove_branch_protections(self):
        set_module_args({
            'access_token': 'test_token',
            'organization': 'org_name',
            'repository': 'test_repo_protected',
            'branch': 'test_branch_protected',
            'branch_protections': {
                'strict': True,
                'contexts': ['defaults'],
                'enforce_admins': False,
                'dismissal_users': [],
                'dismissal_teams': [],
                'dismiss_stale_reviews': False,
                'require_code_owner_reviews': False,
                'required_approving_review_count': 0,
                'user_push_restrictions': [],
                'team_push_restrictions': [],
            },
            'state': 'absent'
        })
        test = {}
        result, changed = run_module()
        assert result == test
        assert changed is True

    def test_remove_branch_protections_from_branch_with_no_protections(self):
        set_module_args({
            'access_token': 'test_token',
            'organization': 'org_name',
            'repository': 'test_repo_NOT_protected',
            'branch': 'test_branch_protected',
            'branch_protections': {
                'strict': True,
                'contexts': ['defaults'],
                'enforce_admins': False,
                'dismissal_users': [],
                'dismissal_teams': [],
                'dismiss_stale_reviews': False,
                'require_code_owner_reviews': False,
                'required_approving_review_count': 0,
                'user_push_restrictions': [],
                'team_push_restrictions': [],
            },
            'state': 'absent'
        })
        test = {}
        result, changed = run_module()
        assert result == test
        assert changed is True

    def test_editing_branch_protection_with_same_protections_check_mode(self):
        set_module_args({
            'access_token': 'test_token',
            'organization': 'org_name',
            'repository': 'test_repo_protected',
            'branch': 'test_branch_protected',
            'branch_protections': {
                'strict': False,
                'contexts': [],
                'enforce_admins': False,
                'dismissal_users': [],
                'dismissal_teams': [],
                'dismiss_stale_reviews': False,
                'require_code_owner_reviews': False,
                'required_approving_review_count': 0,
                'user_push_restrictions': [],
                'team_push_restrictions': [],
            },
            'state': 'present',
            'check_mode': True
        })
        result, changed = run_module()
        test = {
            "allow_deletions": {
                "enabled": False
            },
            "allow_force_pushes": {
                "enabled": False
            },
            "enforce_admins": {
                "enabled": False,
                "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/enforce_admins"
            },
            "required_conversation_resolution": {
                "enabled": False
            },
            "required_linear_history": {
                "enabled": False
            },
            "required_pull_request_reviews": {
                "dismiss_stale_reviews": False,
                "dismissal_restrictions": {
                    "teams": [],
                    "teams_url": "https://api.github.com/repos/org_name/test_repo_protected/" +
                                 "branches/test_branch_protected/protection/dismissal_restrictions/teams",
                    "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/dismissal_restrictions",
                    "users": [],
                    "users_url": "https://api.github.com/repos/org_name/test_repo_protected/" +
                                 "branches/test_branch_protected/protection/dismissal_restrictions/users"
                },
                "require_code_owner_reviews": False,
                "required_approving_review_count": 0,
                "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/required_pull_request_reviews"
            },
            "required_signatures": {
                "enabled": False,
                "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/required_signatures"
            },
            "required_status_checks": {
                "contexts": [],
                "contexts_url": "https://api.github.com/repos/org_name/test_repo_protected/" +
                                "branches/test_branch_protected/protection/required_status_checks/contexts",
                "strict": False,
                "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/required_status_checks"
            },
            "restrictions": {
                "apps": [],
                "apps_url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/restrictions/apps",
                "teams": [],
                "teams_url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/restrictions/teams",
                "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/restrictions",
                "users": [],
                "users_url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/restrictions/users"
            },
            "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection"
        }
        assert result == test
        assert changed is False

    def test_editing_branch_protection_check_mode(self):
        set_module_args({
            'access_token': 'test_token',
            'organization': 'org_name',
            'repository': 'test_repo_protected',
            'branch': 'test_branch_protected',
            'branch_protections': {
                'strict': True,
                'contexts': ['defaults'],
                'enforce_admins': True,
                'dismissal_users': ['test_user'],
                'dismissal_teams': ['test_team'],
                'dismiss_stale_reviews': True,
                'require_code_owner_reviews': True,
                'required_approving_review_count': 100,
                'user_push_restrictions': [],
                'team_push_restrictions': [],
            },
            'state': 'present',
            'check_mode': True
        })
        result, changed = run_module()
        test = {
            "allow_deletions": {
                "enabled": False
            },
            "allow_force_pushes": {
                "enabled": False
            },
            "enforce_admins": {
                "enabled": True,
                "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/enforce_admins"
            },
            "required_conversation_resolution": {
                "enabled": False
            },
            "required_linear_history": {
                "enabled": False
            },
            "required_pull_request_reviews": {
                "dismiss_stale_reviews": True,
                "dismissal_restrictions": {
                    "teams": ['test_team'],
                    "teams_url": "https://api.github.com/repos/org_name/test_repo_protected/" +
                                 "branches/test_branch_protected/protection/dismissal_restrictions/teams",
                    "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/dismissal_restrictions",
                    "users": ['test_user'],
                    "users_url": "https://api.github.com/repos/org_name/test_repo_protected/" +
                                 "branches/test_branch_protected/protection/dismissal_restrictions/users"
                },
                "require_code_owner_reviews": True,
                "required_approving_review_count": 100,
                "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/required_pull_request_reviews"
            },
            "required_signatures": {
                "enabled": False,
                "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/required_signatures"
            },
            "required_status_checks": {
                "contexts": ['defaults'],
                "contexts_url": "https://api.github.com/repos/org_name/test_repo_protected/" +
                                "branches/test_branch_protected/protection/required_status_checks/contexts",
                "strict": True,
                "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/required_status_checks"
            },
            "restrictions": {
                "apps": [],
                "apps_url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/restrictions/apps",
                "teams": [],
                "teams_url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/restrictions/teams",
                "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/restrictions",
                "users": [],
                "users_url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection/restrictions/users"
            },
            "url": "https://api.github.com/repos/org_name/test_repo_protected/branches/test_branch_protected/protection"
        }
        assert result == test
        assert changed is True

    def test_remove_branch_protections_check_mode(self):
        set_module_args({
            'access_token': 'test_token',
            'organization': 'org_name',
            'repository': 'test_repo_protected',
            'branch': 'test_branch_protected',
            'branch_protections': {
                'strict': True,
                'contexts': ['defaults'],
                'enforce_admins': False,
                'dismissal_users': [],
                'dismissal_teams': [],
                'dismiss_stale_reviews': False,
                'require_code_owner_reviews': False,
                'required_approving_review_count': 0,
                'user_push_restrictions': [],
                'team_push_restrictions': [],
            },
            'state': 'absent',
            'check_mode': True
        })
        test = {}
        result, changed = run_module()
        assert result == test
        assert changed is True

    def test_remove_branch_protections_from_branch_with_no_protections_check_mode(self):
        set_module_args({
            'access_token': 'test_token',
            'organization': 'org_name',
            'repository': 'test_repo_NOT_protected',
            'branch': 'test_branch_protected',
            'branch_protections': {
                'strict': True,
                'contexts': ['defaults'],
                'enforce_admins': False,
                'dismissal_users': [],
                'dismissal_teams': [],
                'dismiss_stale_reviews': False,
                'require_code_owner_reviews': False,
                'required_approving_review_count': 0,
                'user_push_restrictions': [],
                'team_push_restrictions': [],
            },
            'state': 'absent',
            'check_mode': True
        })
        test = {}
        result, changed = run_module()
        assert result == test
        assert changed is True
